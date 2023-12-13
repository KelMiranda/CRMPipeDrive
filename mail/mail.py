import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Mail:
    def __init__(self, smtp_server, username, password):
        self.smtp_server = os.getenv(smtp_server)
        self.username = os.getenv(username)
        self.password = os.getenv(password)

    def enviar_correo(self, destinatario, asunto, mensaje):
        # Crear objeto de mensaje
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = destinatario
        msg['Subject'] = asunto
        msg.attach(MIMEText(mensaje, 'html'))

        server = None  # Inicializar la variable del servidor

        try:
            # Intentar establecer la conexión y enviar el correo
            server = smtplib.SMTP(self.smtp_server, 587)
            server.starttls()
            server.login(self.username, self.password)
            server.sendmail(self.username, destinatario, msg.as_string())
            print('Correo electrónico enviado exitosamente.')
        except smtplib.SMTPException as e:
            print('Error al enviar el correo electrónico:', str(e))
        finally:
            # Asegurar que la conexión se cierre correctamente
            if server is not None:
                try:
                    server.quit()
                except smtplib.SMTPServerDisconnected:
                    print('La conexión con el servidor SMTP ya estaba cerrada.')
                except Exception as e:
                    print('Error al cerrar la conexión con el servidor SMTP:', str(e))