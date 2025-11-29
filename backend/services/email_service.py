"""
Email Service - Send emails via SMTP
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import settings
from typing import Optional
import asyncio
from concurrent.futures import ThreadPoolExecutor


class EmailService:
    """Service for sending emails"""
    
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=5)
    
    async def send_application_confirmation(
        self,
        to_email: str,
        candidato_nombre: str,
        vacante_titulo: str,
        empresa_nombre: str,
        puntuacion: int
    ) -> bool:
        """
        Send application confirmation email to candidate
        
        Args:
            to_email: Candidate's email
            candidato_nombre: Candidate's name
            vacante_titulo: Job title
            empresa_nombre: Company name
            puntuacion: AI score
            
        Returns:
            True if email sent successfully
        """
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"Confirmación de aplicación - {vacante_titulo}"
            msg['From'] = settings.email_from or settings.smtp_user
            msg['To'] = to_email
            
            # Email body
            html = f"""
            <html>
              <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                  <h2 style="color: #2563eb;">¡Aplicación Recibida!</h2>
                  
                  <p>Hola <strong>{candidato_nombre}</strong>,</p>
                  
                  <p>Hemos recibido exitosamente tu aplicación para la posición de:</p>
                  
                  <div style="background-color: #f3f4f6; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin: 0; color: #1f2937;">{vacante_titulo}</h3>
                    <p style="margin: 5px 0; color: #6b7280;">en {empresa_nombre}</p>
                  </div>
                  
                  <p>Tu perfil ha sido evaluado por nuestro sistema de IA y obtuvo una puntuación de <strong>{puntuacion}/100</strong>.</p>
                  
                  <p>El equipo de reclutamiento revisará tu aplicación y te contactaremos pronto si tu perfil es seleccionado para la siguiente etapa.</p>
                  
                  <p style="margin-top: 30px;">¡Mucha suerte!</p>
                  
                  <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 30px 0;">
                  
                  <p style="font-size: 12px; color: #6b7280;">
                    Este es un correo automático, por favor no responder.
                  </p>
                </div>
              </body>
            </html>
            """
            
            text = f"""
            ¡Aplicación Recibida!
            
            Hola {candidato_nombre},
            
            Hemos recibido exitosamente tu aplicación para la posición de:
            {vacante_titulo} en {empresa_nombre}
            
            Tu perfil ha sido evaluado por nuestro sistema de IA y obtuvo una puntuación de {puntuacion}/100.
            
            El equipo de reclutamiento revisará tu aplicación y te contactaremos pronto si tu perfil es seleccionado.
            
            ¡Mucha suerte!
            """
            
            part1 = MIMEText(text, 'plain')
            part2 = MIMEText(html, 'html')
            
            msg.attach(part1)
            msg.attach(part2)
            
            # Send email
            if not settings.smtp_user or not settings.smtp_password:
                print("SMTP credentials not configured, skipping email")
                return False
            
            # Run SMTP operation in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                self.executor,
                self._send_smtp,
                settings.smtp_host,
                settings.smtp_port,
                settings.smtp_user,
                settings.smtp_password,
                msg,
                to_email
            )
            return result
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def _send_smtp(self, host: str, port: int, user: str, password: str, msg: MIMEMultipart, to_email: str) -> bool:
        """Helper method to send SMTP email synchronously"""
        try:
            with smtplib.SMTP(host, port) as server:
                server.starttls()
                server.login(user, password)
                server.send_message(msg)
            
            print(f"Email sent successfully to {to_email}")
            return True
        except Exception as e:
            print(f"Error in SMTP operation: {e}")
            return False


# Singleton instance
email_service = EmailService()
