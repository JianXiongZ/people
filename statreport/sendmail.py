#!/usr/bin/env python
import smtplib
import uuid
from email.mime.multipart import MIMEMultipart
from email.mime.text      import MIMEText
from email.mime.image     import MIMEImage
import os



def post(mail):
	me=mail['user']+"<"+mail['from_address']+">"
	msg = MIMEMultipart('related')
	msg['Subject'] = mail['subject']
	msg['From'] = me
	msg['To'] = mail['to_list']
	to_list = mail['to_list'].split(';')
	msg_alternative = MIMEMultipart('alternative')
	msg.attach(msg_alternative)
	
	if 'img' in mail:
		img = dict(path=mail['img'], cid=str(uuid.uuid4()))
		msg_html = MIMEText(mail['content'].replace('$IMG_CID$',img['cid']),'HTML')
		msg_alternative.attach(msg_html)

		with open(img['path'], 'rb') as file:
			msg_image = MIMEImage(file.read(), name=os.path.basename(img['path']))
			msg.attach(msg_image)
		msg_image.add_header('Content-ID', '<{}>'.format(img['cid']))
	else:
		msg_html = MIMEText(mail['content'],'HTML')
		msg_alternative.attach(msg_html)
	
	try:
		s = smtplib.SMTP()
		s.connect(mail['smtp_server'])
		s.login(mail['user'],mail['password'])
		s.sendmail(me, to_list, msg.as_string())
		s.close()
		return True
	except Exception, e:
		print str(e)
		return False




def post2(mail):

	me=mail['user']+"<"+mail['from_address']+">"
	msg = MIMEMultipart('related')
	msg.attach(MIMEText(mail['content'],'HTML'))
	msg['Subject'] = mail['subject']
	msg['From'] = me
	msg['To'] = mail['to_list']
	to_list = mail['to_list'].split(';')
	
	adjuntoImagen_1 = MIMEBase('application', "octet-stream")
	adjuntoImagen_1.set_payload(open(mail['img'], "rb").read())
	encode_base64(adjuntoImagen_1)
	anexoImagen_1 = os.path.basename(mail['img'])
	adjuntoImagen_1.add_header('Content-Disposition', 'attachment; filename= "%s"' % anexoImagen_1)
	msg.attach(adjuntoImagen_1)
	
	
	try:
		s = smtplib.SMTP()
		s.connect(mail['smtp_server'])
		s.login(mail['user'],mail['password'])
		s.sendmail(me, to_list, msg.as_string())
		s.close()
		return True
	except Exception, e:
		print str(e)
		return False
def sendmail(time,data,cfg):
	mail = cfg['Email'] 


	mail['user'] = mail['from_address'].split('@')[0]
	mail['subject'] = "[Miner Status " + cfg['Miner']['server_code'] + "] Report " + time

		
	mail['content'] = '''\
<html>
  <head>
    <meta content="text/html; charset=gbk" http-equiv="content-type">
    <base target="_blank">
  </head>
  <body style="        margin-bottom: 0px; margin-top: 0px; padding-bottom: 0px; padding-top: 0px;">
    <div style="background-color: #f5f5f5;width:100%;-webkit-text-size-adjust:none !important;margin:0;padding: 70px 0 70px 0;">
      <table border="0" cellpadding="0" cellspacing="0" height="100%" width="100%">
        <tbody>
          <tr>
            <td align="center" valign="top">
              <table id="template_container" style="-webkit-box-shadow:0 0 0 3px rgba(0,0,0,0.025) !important;box-shadow:0 0 0 3px rgba(0,0,0,0.025) !important;-webkit-border-radius:6px !important;border-radius:6px !important;	background-color: #fdfdfd;border: 1px solid #dcdcdc;-webkit-border-radius:6px !important;border-radius:6px !important;"
                border="0" cellpadding="0" cellspacing="0" width="600">
                <tbody>
                  <tr>
                    <td align="center" valign="top">
                      <table id="template_header" style="background-color: #557da1; color: white; border-top-left-radius: 6px ! important; border-top-right-radius: 6px ! important; border-bottom: 0px none; font-family: Arial; font-weight: bold; line-height: 100%; vertical-align: middle; width: 600px; height: 102px;"
                        border="0" cellpadding="0" cellspacing="0">
                        <tbody>
                          <tr>
                            <td>
                              <h1 style="color: white; margin: 0px; padding: 28px 24px; text-shadow: 0px 1px 0px #7797b4; display: block; font-family: Arial; font-size: 30px; font-weight: bold; text-align: left; line-height: 10%;">Miner
                                Status Report</h1>
                            </td>
                          </tr>
                          <tr align="right">
                            <td style="margin-left: -200px;"><span style="font-weight: normal; font-size: smaller;">'''
                            
	mail['content'] += "Server: " + cfg['Miner']['server_code'] + "&nbsp;&nbsp;&nbsp;&nbsp; " + time
	mail['content'] +='''&nbsp;&nbsp;&nbsp;&nbsp; </span></td>
                          </tr>
                        </tbody>
                      </table>
                    </td>
                  </tr>
                  <tr>
                    <td align="center" valign="top">
                      <table id="template_body" border="0" cellpadding="0" cellspacing="0"
                        width="600">
                        <tbody>
                          <tr>
                            <td style="background-color: #fdfdfd;	-webkit-border-radius:6px !important;border-radius:6px !important;"
                              valign="top">
                              <table border="0" cellpadding="20" cellspacing="0"
                                width="100%">
                                <tbody>
                                  <tr>
                                    <td valign="top">
                                      <div style="color: #737373;	font-family:Arial;	font-size:14px;	line-height:150%;text-align:left;">
                                        <p style="text-align: center;"><a href="https://cex.io/r/0/canaan/0/"
                                            title="CEX.IO - Trade Ghashes while they mine you Bitcoins!"
                                            target="_blank"> <img src="http://cex.io/informer/canaan/286ea7ed8c69fe6c98fcefeccb273fab/"
                                              border="0" height="35" width="500"></a></p>
                                        <p>
                                          <meta http-equiv="content-type" content="text/html; charset=utf-8">
                                        </p>
                                      </div>
                                    </td>
                                  </tr>
                                  <tr>
                                    <td><span style="color: black; font-size: large;"><span
                                          style="font-weight: bold;">Active IP:</span>
                                        &nbsp;&nbsp;&nbsp; '''
	alivenum = 0
	for miner in data:
		if miner[1] == "Alive":
			alivenum += 1
	mail['content'] += str(alivenum) + '/' + str(len(cfg['Miner']['miner_list']))

	mail['content'] += '''</span></td>
                                  </tr>
                                  <tr>
                                    <td><span style="font-weight: bold; color: black; font-size: large;">Errant
                                        Modules List:</span><span style="font-weight: bold; color: black; font-size: large;"><br>
                                      </span>
                                      <table style="width: 100%; border: 1px solid #eeeeee;"
                                        border="1" bordercolor="#eee" cellpadding="6"
                                        cellspacing="0">
                                        <tfoot>
                                          <tr>
                                            <th scope="col" style="text-align: left; border: 1px solid #eeeeee; width: 264px;">Miner
                                              IP</th>
                                            <th scope="col" style="text-align: left; border: 1px solid #eeeeee; margin-left: -169px;">Alive
                                              Modules Number<br>
                                            </th>
                                          </tr>'''
		
	for miner in data:
		sum_mod_num = 0
		for dev_stat in miner[4]:
			sum_mod_num += dev_stat[3]
		if sum_mod_num < int(cfg['Miner']['module_number']):
			mail['content'] += '''<tr>
                                            <th scope="row" colspan="1" style="text-align:left; border: 1px solid #eee; border-top-width: 4px;"><span
                                                style="font-weight: normal;">''' + miner[0] + '''</th>
                                            <td style="text-align:left; border: 1px solid #eee;	border-top-width: 4px;"><span
                                                class="amount">''' + str(sum_mod_num) + "/" + cfg['Miner']['module_number'] + "</span></td></tr>"
	mail['content'] += '''</tfoot>
                                      </table>
                                    </td>
                                  </tr>'''
	if 'img' in mail:
		mail['content'] += '''\
                                  <tr>
                                    <td><img src=cid:''' + "$IMG_CID$" + '''><br>
                                    </td>
                                  </tr>'''
	mail['content'] += '''\
                                </tbody>
                              </table>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </td>
                  </tr>
                </tbody>
              </table>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </body>
</html>''' 
	if post(mail):
		print "Successed in sending email."
	else:
		print "Failed in sending email."

if __name__ == '__main__':
	print 0
        
