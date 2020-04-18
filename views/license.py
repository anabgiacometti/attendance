from app import app, db
from flask import render_template, redirect, url_for, request, abort, session, jsonify, send_file
from models.license import License, LicenseFiles
from models.client import Client
from models.system import System
from forms.licenses import LicenseForm
from flask_paginate import Pagination, get_page_parameter
from collections import OrderedDict
from io import BytesIO

@app.route('/licenses')
def Licenses():
    if 'userid' not in session or session['userid'] == None or 'client' not in session or session['client'] != None:
        return redirect(url_for('Login'))

    else:
        admin = session['admin']
        q = request.args.get('q')
        
        if q:
            licenses = License.query.order_by(License.date).join('client').join('system')\
                .filter(License.deleted == False)\
                    .filter( (Client.cnpj.like('%' + q + '%')) | (Client.cpf.like('%' + q + '%')) | (Client.bussiness_name.like('%' + q + '%')) | (System.name.like('%' + q + '%')) )
        else:
            licenses = License.query.order_by(License.date).filter(License.deleted == False)

        page = request.args.get(get_page_parameter(), type=int, default=1)

        license_list = licenses.offset(5 * (page-1)).limit(5)

        pagination = Pagination(page=page, total=licenses.count(), search=False, record_name='license', per_page=5)

        if not q:
            q = ""

        message = None

        if 'message' in session and session['message'] != None:
            message = session['message']
            session['message'] = None

        return render_template('license/index.html', admin=admin, licenses=license_list, pagination=pagination, search=q, message=message)



@app.route('/license', methods=["GET", "POST"])
def UniqueLicense():
    if 'userid' not in session or session['userid'] == None or 'client' not in session or session['client'] != None:
        return redirect(url_for('Login'))
    
    else:
        admin = session['admin']
        form = LicenseForm()
        client_name = ""
        reseller_name = ""

        systems = System.query.filter_by(deleted=False).all()
        system_list=[("{}".format(i.id), i.name) for i in systems]
        
        form.system.choices = system_list

        if request.method == "POST" and form.validate_on_submit():

            if not form.id.data:
                service_db = License.query.filter(License.deleted == False).filter(License.client_id == form.client.data)\
                    .filter(License.system_id == form.system.data).first()

                if form.client.data: 
                    client = Client.query.filter(Client.id == form.client.data).first()
                    identifier = client.cpf if client.type == 2 else client.cnpj
                    client_name = "{} - {}".format(identifier, client.bussiness_name)
                
                if service_db: 
                    if form.client.data: 
                        client = Client.query.filter(Client.id == form.client.data).first()
                        identifier = client.cpf if client.type == 2 else client.cnpj
                        client_name = "{} - {}".format(identifier, client.bussiness_name)
                    form.client.errors.append('Já existe uma licença deste sistema para este cliente.')
                    return render_template('license/license.html',admin=admin, form=form, client_name=client_name, reseller_name=reseller_name, isreseller=isreseller)

                if form.resale.data == "0": 
                    isreseller = "1"
                    form.resale.errors.append('Selecione um revendedor.')
                    return render_template('license/license.html',admin=admin, form=form, client_name=client_name, reseller_name=reseller_name, isreseller=isreseller)

                else:

                    resale = False

                    if form.resale.data != "":
                        resale = True

                    new_license = License(
                        client_id = form.client.data,
                        system_id = form.system.data, 
                        date = form.date.data, 
                        instalation_tech = form.instalation_tech.data,
                        training_tech = form.training_tech.data, 
                        training_client = form.training_client.data,
                        obs = form.obs.data,
                        deleted = False,
                        seller = form.seller.data, 
                        serial_number = form.serial_number.data, 
                        fabric_number = form.fabric_number.data, 
                        resale = resale, 
                    )

                    if resale:
                        new_license.reseller_id = form.resale.data
                        new_license.reseller_name = Client.query.filter(Client.id == form.resale.data).first().bussiness_name

                    db.session.add(new_license)
                    db.session.commit()

                    for file in form.attachments.data:
                        if file.filename:
                            newFile = LicenseFiles(
                                name = file.filename, 
                                data = file.read(), 
                                license_id = new_license.id, 
                                deleted = False
                            )
                            db.session.add(newFile)
                            db.session.commit()                        
                        
                    session['message'] = "Licença cadastrada!"

                    return redirect(url_for('Licenses'))

            else:
                license_db = License.query.filter(License.id == form.id.data).first()
                license_duplicated = License.query.filter(License.deleted == False).filter(License.client_id == form.client.data)\
                    .filter(License.system_id == form.system.data).filter(License.id != form.id.data).first()    

                if license_duplicated: 
                    form.client.errors.append('Já existe uma licença deste sistema para este cliente.')
                    identifier = license_db.client.cpf if license_db.client.type == 2 else license_db.client.cnpj
                    client_name = "{} - {}".format(identifier, license_db.client.bussiness_name)
                    form.system.choices = system_list
                    return render_template('license/license.html',admin=admin, form=form, client_name=client_name, reseller_name=reseller_name, sys_val=license.system_id, files=license.files, isreseller=isreseller)
                    
                license_db.client_id = form.client.data
                license_db.system_id = form.system.data 
                license_db.date = form.date.data
                license_db.instalation_tech = form.instalation_tech.data
                license_db.training_tech = form.training_tech.data
                license_db.training_client = form.training_client.data
                license_db.obs = form.obs.data                
                license_db.seller = form.seller.data                
                license_db.fabric_number = form.fabric_number.data                
                license_db.serial_number = form.serial_number.data                
                
                for file in form.attachments.data:
                    if file.filename:
                        newFile = LicenseFiles(
                            name = file.filename, 
                            data = file.read(), 
                            license_id = license_db.id, 
                            deleted = False
                        )
                        db.session.add(newFile)
                        
                db.session.commit()

                session['message'] = "Alterações salvas!"

                return redirect(url_for('Licenses'))
        
        else:
            licenseid = request.args.get('license')
            isreseller = request.args.get('reseller')
            if isreseller == "1":
                form.resale.data = 0

            if licenseid:        
                license = License.query.join(Client).join(System).filter(License.id == licenseid).first()
                form = LicenseForm(obj=license)

                identifier = license.client.cpf if license.client.type == 2 else license.client.cnpj
                client_name = "{} - {}".format(identifier, license.client.bussiness_name)              

                if license.resale:
                    isreseller = "1"
                    reseller = Client.query.filter(Client.id == license.reseller_id).first()
                    reseller_id = reseller.cpf if reseller.type == 2 else reseller.cnpj
                    reseller_name = "{} - {}".format(reseller_id, reseller.bussiness_name)

                form.resale.data = license.reseller_id
                form.system.choices = system_list
                form.client.data = license.client.id

                return render_template('license/license.html',admin=admin, form=form, client_name=client_name, reseller_name=reseller_name, sys_val=license.system_id, files=license.files, isreseller=isreseller)
            
        if form.client.data: 
            client = Client.query.filter(Client.id == form.client.data).first()
            identifier = client.cpf if client.type == 2 else client.cnpj
            client_name = "{} - {}".format(identifier, client.bussiness_name)
       
        return render_template('license/license.html',admin=admin, form=form, client_name=client_name, reseller_name=reseller_name, isreseller=isreseller)


@app.route('/getclients')
def GetClients():
    clients = Client.query.filter(Client.resale == False).filter(Client.deleted == False).all()
    clients_list = []

    for client in clients:
        identifier = client.cpf if client.type == 2 else client.cnpj
        cli = { "id": client.id, "name": "{} - {}".format(identifier, client.bussiness_name), "resale": False }
        clients_list.append(cli)

    return jsonify(clients_list)


@app.route('/getresellers')
def GetResellers():
    resellers = Client.query.filter(Client.resale == True).filter(Client.deleted == False).all()
    resellers_list = []

    for reseller in resellers:
        identifier = reseller.cpf if reseller.type == 2 else reseller.cnpj
        cli = { "id": reseller.id, "name": "{} - {}".format(identifier, reseller.bussiness_name), "resale": True }
        resellers_list.append(cli)

    return jsonify(resellers_list)


@app.route('/dellicense/<id>')
def DeleteLicense(id):
    if 'userid' not in session or session['userid'] == None or 'client' not in session or session['client'] != None:
        return redirect(url_for('Login'))
    
    else:
        license = License.query.filter(License.id == id).first()
        license.deleted = True
        db.session.commit()

        session['message'] = "Licença excluída!"

        return redirect(url_for('Licenses'))


@app.route('/download-license-file/<id>')
def DownloadLicenseFile(id):
    file = LicenseFiles.query.filter(LicenseFiles.id == id).first()
    return send_file(BytesIO(file.data), attachment_filename=file.name, as_attachment=True)