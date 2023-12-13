from mail.mail import Mail


if __name__ == '__main__':
    mail = Mail('SMTP_SERVER',  'SMTP_USERNAME', 'SMTP_PASSWORD')
    mail.enviar_correo('kelvin.miranda@grupopelsa.com', 'test', '<p>Contenido del mensaje en HTML</p>')
