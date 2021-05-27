# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from carService.models import Car, ServiceSituation, ServiceProduct, Service
from carService.models.Setting import Setting


def send_mail(service, to):
    if service.car.profile.isSendMail:
        situation = ServiceSituation.objects.filter(service=service).order_by('-id')[:1][
            0].situation.name
        car = Car.objects.get(uuid=service.car.uuid)
        logo = Setting.objects.get(key="logo-dark").value
        site_link = Setting.objects.get(key="site-link").value
        car_model = car.model
        car_brand = car.brand
        service_products = ServiceProduct.objects.filter(service=service)
        products = []

        for serviceProduct in service_products:
            isExist = False
            for productArr in products:
                if serviceProduct.product.uuid == productArr.uuid:
                    productArr.quantity = productArr.quantity + serviceProduct.quantity
                    productArr.netPrice = serviceProduct.productNetPrice * productArr.quantity
                    isExist = True

            if not isExist:
                product = serviceProduct.product
                product.netPrice = serviceProduct.productNetPrice
                product.totalProduct = serviceProduct.productTotalPrice
                product.taxRate = serviceProduct.productTaxRate
                product.quantity = serviceProduct.quantity
                products.append(product)
        labor = ServiceProduct.product
        labor.barcodeNumber = '-'
        labor.name = service.laborName
        labor.brand = None
        labor.quantity = 1
        labor.netPrice = service.laborPrice
        labor.taxRate = service.laborTaxRate
        labor.totalProduct = (
                float(service.laborPrice) + (float(service.laborPrice) * float(service.laborTaxRate) / 100))
        if labor.name != None:
            products.append(labor)
        profile = car.profile
        receiver = "-"
        if service.receiverPerson != None:
            receiver = service.receiverPerson
        name = ""
        product_table = ""

        for product in products:
            brand_name = ""
            if product.brand != None:
                brand_name = product.brand.name
            product_table = product_table + '''<tr>
                         <td style="font-size: 12px; border-right: 1px solid #DDDDDD; border-bottom: 1px solid #DDDDDD; text-align: left; padding: 7px;">''' + product.barcodeNumber + '''</td>
                         <td style="font-size: 12px; border-right: 1px solid #DDDDDD; border-bottom: 1px solid #DDDDDD; text-align: left; padding: 7px;">''' + product.name + '''</td>
                         <td style="font-size: 12px;   border-right: 1px solid #DDDDDD; border-bottom: 1px solid #DDDDDD; text-align: right; padding: 7px;">''' + brand_name + '''</td>
                         <td style="font-size: 12px;   border-right: 1px solid #DDDDDD; border-bottom: 1px solid #DDDDDD; text-align: right; padding: 7px;">''' + str(
                product.quantity) + '''</td>
                         <td style="font-size: 12px;   border-right: 1px solid #DDDDDD; border-bottom: 1px solid #DDDDDD; text-align: right; padding: 7px;">''' + str(
                product.netPrice) + '''</td>
                         <td style="font-size: 12px;   border-right: 1px solid #DDDDDD; border-bottom: 1px solid #DDDDDD; text-align: right; padding: 7px;">''' + str(
                product.taxRate) + '''</td>
                         <td style="font-size: 12px;   border-right: 1px solid #DDDDDD; border-bottom: 1px solid #DDDDDD; text-align: right; padding: 7px;">''' + str(
                product.totalProduct) + '''</td>
                       </tr>'''
        if situation == "Müşteri Onayı Bekleniyor":
            product_table = '''
            <table style="border-collapse: collapse; width: 100%; border-top: 1px solid #DDDDDD; border-left: 1px solid #DDDDDD; margin-bottom: 20px;">
               <thead>
                 <tr>
                   <td style="font-size: 12px; border-right: 1px solid #DDDDDD; border-bottom: 1px solid #DDDDDD; background-color: #EFEFEF; font-weight: bold; text-align: left; padding: 7px; color: #222222;" colspan="2">''' + "Şikayet" + '''</td>
                 </tr>
               </thead>
               <tbody>
                  <tr>
                   <td style="font-size: 12px;	border-right: 1px solid #DDDDDD; border-bottom: 1px solid #DDDDDD; text-align: left; padding: 7px;"><b>Müşteri</b>''' + profile.firmName + "-" + \
                            profile.user.first_name + " " + profile.user.last_name + '''<br />
                     <b>Servise Getiren:</b> ''' + service.responsiblePerson + '''<br />
                     <b>Plaka:</b> ''' + car.plate + '''<br/>
                     <b>Marka/Model:</b> ''' + car_brand + '''/''' + car_model + '''</td>
                   <td style="font-size: 12px;	border-right: 1px solid #DDDDDD; border-bottom: 1px solid #DDDDDD; text-align: left; padding: 7px;"><b>Kilometre:</b>''' + str(
                service.serviceKM) + '''<br />
                     <b>Giriş zamanı:</b> ''' + str(service.creationDate).split(".")[0] + '''<br />
                     <b>Teslim Alan:</b> ''' + receiver + '''<br /></td>
                 </tr>
               </tbody>
             </table>
            <table style="border-collapse: collapse; width: 100%; border-top: 1px solid #DDDDDD; border-left: 1px solid #DDDDDD; margin-bottom: 20px;">
               <thead>
                 <tr>
                   <td style="font-size: 12px; border-right: 1px solid #DDDDDD; border-bottom: 1px solid #DDDDDD; background-color: #EFEFEF; font-weight: bold; text-align: left; padding: 7px; color: #222222;" colspan="2">''' + "Şikayet" + '''</td>
                 </tr>
               </thead>
               <tbody>
                 <tr>
                   <td style="font-size: 12px;	border-right: 1px solid #DDDDDD; border-bottom: 1px solid #DDDDDD; text-align: left; padding: 7px;">''' + service.complaint + '''</td>
                 </tr>
               </tbody>
             </table>
            <table style="border-collapse: collapse; width: 100%; border-top: 1px solid #DDDDDD; border-left: 1px solid #DDDDDD; margin-bottom: 20px;">
               <thead>
                 <tr>
                   <td style="font-size: 12px; border-right: 1px solid #DDDDDD; border-bottom: 1px solid #DDDDDD; background-color: #EFEFEF; font-weight: bold; text-align: left; padding: 7px; color: #222222;" colspan="2">''' + "Tespit" + '''</td>
                 </tr>
               </thead>
               <tbody>
                 <tr>
                   <td style="font-size: 12px;	border-right: 1px solid #DDDDDD; border-bottom: 1px solid #DDDDDD; text-align: left; padding: 7px;">''' + service.description + '''</td>
                 </tr>
               </tbody>
             </table>
             <table style="border-collapse: collapse; width: 100%; border-top: 1px solid #DDDDDD; border-left: 1px solid #DDDDDD; margin-bottom: 20px;">
               <thead>
                 <tr>
                   <td style="font-size: 12px; border-right: 1px solid #DDDDDD; border-bottom: 1px solid #DDDDDD; background-color: #EFEFEF; font-weight: bold; text-align: left; padding: 7px; color: #222222;">Barkod Numarası:</td>
                   <td style="font-size: 12px; border-right: 1px solid #DDDDDD; border-bottom: 1px solid #DDDDDD; background-color: #EFEFEF; font-weight: bold; text-align: left; padding: 7px; color: #222222;">Ürün Adı:</td>
                   <td style="font-size: 12px; border-right: 1px solid #DDDDDD; border-bottom: 1px solid #DDDDDD; background-color: #EFEFEF; font-weight: bold; text-align: right; padding: 7px; color: #222222;">Marka:</td>
                   <td style="font-size: 12px; border-right: 1px solid #DDDDDD; border-bottom: 1px solid #DDDDDD; background-color: #EFEFEF; font-weight: bold; text-align: right; padding: 7px; color: #222222;">Adet:</td>
                   <td style="font-size: 12px; border-right: 1px solid #DDDDDD; border-bottom: 1px solid #DDDDDD; background-color: #EFEFEF; font-weight: bold; text-align: right; padding: 7px; color: #222222;">Net Fiyat:</td>
                   <td style="font-size: 12px; border-right: 1px solid #DDDDDD; border-bottom: 1px solid #DDDDDD; background-color: #EFEFEF; font-weight: bold; text-align: right; padding: 7px; color: #222222;">Vergi Oranı:</td>
                   <td style="font-size: 12px; border-right: 1px solid #DDDDDD; border-bottom: 1px solid #DDDDDD; background-color: #EFEFEF; font-weight: bold; text-align: right; padding: 7px; color: #222222;">Toplam Fiyat:</td>
                 </tr>
               </thead>
               <tbody>
             ''' + product_table + '''</tbody>
               <tfoot>
               <tr>
                 <td style="font-size: 12px;	border-right: 1px solid #DDDDDD; border-bottom: 1px solid #DDDDDD; text-align: left; padding: 7px;" colspan="4"><b>Net Fiyat:     </b>''' + str(
                service.price) + '''</td>
                 <td style="font-size: 12px;	border-right: 1px solid #DDDDDD; border-bottom: 1px solid #DDDDDD; text-align: left; padding: 7px;" colspan="4"><b>Toplam Fiyat:     </b>''' + str(
                service.totalPrice) + '''</td>
               </tr>
               </tfoot>
             </table>'''
        elif situation == "Tamamlandı":
            product_table = '''
            <table style="border-collapse: collapse; width: 40%; border-top: 1px solid #DDDDDD; border-left: 1px solid #DDDDDD; margin-bottom: 20px;">
               <thead>
                 <tr>
                   <td style="font-size: 12px; border-right: 1px solid #DDDDDD; border-bottom: 1px solid #DDDDDD; background-color: #EFEFEF; font-weight: bold; text-align: left; padding: 7px; color: #222222;" colspan="2">''' + "DURUM" + '''</td>
                 </tr>
               </thead>
               <tbody>
                 <tr>
                   <td style="font-size: 12px;	border-right: 1px solid #DDDDDD; border-bottom: 1px solid #DDDDDD; text-align: left; padding: 7px;">Tamamlandı</td>
                 </tr>
               </tbody>
             </table>
              <div>Aracınıza ait servis işlemi tamamlanmıştır. Teslim almak için lütfen servise geliniz.</div>'''

        elif situation == "Teslim Edildi":
            product_table = '''
            <table style="border-collapse: collapse; width: 40%; border-top: 1px solid #DDDDDD; border-left: 1px solid #DDDDDD; margin-bottom: 20px;">
               <thead>
                 <tr>
                   <td style="font-size: 12px; border-right: 1px solid #DDDDDD; border-bottom: 1px solid #DDDDDD; background-color: #EFEFEF; font-weight: bold; text-align: left; padding: 7px; color: #222222;" colspan="2">''' + "DURUM" + '''</td>
                 </tr>
               </thead>
               <tbody>
                 <tr>
                   <td style="font-size: 12px;	border-right: 1px solid #DDDDDD; border-bottom: 1px solid #DDDDDD; text-align: left; padding: 7px;">Teslim edildi</td>
                 </tr>
               </tbody>
             </table>
                <div>''' + car.plate + '''  plakalı aracınız ''' + receiver + ''' isimli kişiye teslim edilmiştir.</div>    
            '''

        else:
            product_table = ""
        if (profile.firmName):
            name = profile.firmName + "-" + \
                   profile.user.first_name + " " + profile.user.last_name
        else:
            name = profile.user.first_name + " " + profile.user.last_name
        serviceman = service.serviceman.user.first_name + \
                     " " + service.serviceman.user.last_name
        subject, from_email = 'Kulmer Motorlu Araçlar Servis Bilgilendirme', 'servis@kulmer.com.tr'
        text_content = 'Kulmer Motorlu Araçlar Servis Bilgilendirme'

        html = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/1999/REC-html401-19991224/strict.dtd">
           <html>
           <head>
           <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
           </head>
           <body style="font-family: Arial, Helvetica, sans-serif; font-size: 12px; color: #000000;">
            <div style="align-items: center; width: 680px;"><img src="''' + logo + '''" style="margin-left:auto; margin-right:auto; margin-bottom: 20px; width:200px; border: none;" />
             <h3><a href="''' + site_link + '''">Giriş yapmak için tıklayınız</a></h3>
             ''' + product_table + '''
           </div>
           </body>
           </html>'''

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html, "text/html")
        msg.send()


def send_password(password, to):
    # bura mı her yerde gitmiş
    text_content = 'Kulmer Motorlu Araçlar Servis Takip Yazılımı Hesap Bilgileri'
    subject, from_email = 'Kulmer Motorlu Araçlar Servis Takip Yazılımı Hesap Bilgileri', settings.EMAIL_HOST_USER
    logo = Setting.objects.get(key="logo-dark").value
    site_link = Setting.objects.get(key="site-link").value
    html = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/1999/REC-html401-19991224/strict.dtd">
 <html>
  <head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  </head>
    <body style="font-family: Arial, Helvetica, sans-serif; font-size: 12px; color: #000000;">
    <div style="align-items: center; width: 900px;";><a href="''' + logo + '''" title=""><img src="''' + logo + '''" style="margin-left:auto; margin-right:auto; margin-bottom: 20px; width:200px; border: none;" /></a>
    <h3><a href="''' + site_link + '''">Giriş yapmak için tıklayınız:</a></h3>	
    <h4>Merhaba, Kulmer Motorlu Araçlar Servis Takip Sistemine hoşgeldiniz.<br>Aşağıda bulunan kullanıcı adı ve şifrenizle sisteme giriş yapabilirsiniz. <br>Sizleri aramızda görmekten mutluluk duyuyoruz.</h4>
        </div>
    
     <table style="border-collapse: collapse; width: 40%; border-top: 1px solid #DDDDDD; border-left: 1px solid #DDDDDD; margin-bottom: 20px;"> 
               <thead>
                 <tr>
                   <td style="font-size: 12px; border-right: 1px solid #DDDDDD; border-bottom: 1px solid #DDDDDD; background-color: #EFEFEF; font-weight: bold; text-align: left; padding: 7px; color: #222222;">Kullanıcı Adı</td>
                   <td style="font-size: 12px; border-right: 1px solid #DDDDDD; border-bottom: 1px solid #DDDDDD; background-color: #EFEFEF; font-weight: bold; text-align: left; padding: 7px; color: #222222;">Şifre</td>
                 </tr>
               </thead>
               <tbody>
                 <tr>
                   <td style="font-size: 12px;	border-right: 1px solid #DDDDDD; border-bottom: 1px solid #DDDDDD; text-align: left; padding: 7px;">''' + to + '''</td>
                   <td style="font-size: 12px;	border-right: 1px solid #DDDDDD; border-bottom: 1px solid #DDDDDD; text-align: left; padding: 7px;">''' + password + '''</td>
                 </tr>
               </tbody>
             </table>
  </body>
  </html> 
  '''

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html, "text/html")
    msg.send()
