import { Component, OnInit } from '@angular/core';
import { AlertController } from '@ionic/angular';
import { AuthService } from 'src/app/services/auth.service';
import { UsuarioService } from 'src/app/services/usuario.service';
import { ActivatedRoute } from '@angular/router';
import { InvitacionService } from 'src/app/services/invitacion.service';
import { HttpErrorResponse } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-invitar',
  templateUrl: './invitar.component.html',
  styleUrls: ['./invitar.component.scss'],
})
export class InvitarComponent implements OnInit {
  filtro = '';
  errorMensaje: string;
  jugadores: any[] = [];
  id_partido: number;

  constructor(
    private usuarioService: UsuarioService,
    private alertController: AlertController,
    private authService: AuthService,
    private route: ActivatedRoute,
    private invitacionService: InvitacionService,
    private router: Router,
  ) { }

  ngOnInit() {

    this.route.params.subscribe(params => {
      this.id_partido = params['id_partido']; 
      console.log(this.id_partido)     
    });

    this.usuarioService.getUsuarios().subscribe(
      (data: any[]) => {
        this.jugadores = data;
        console.log(this.jugadores);
      },
      (error) => {
        console.log(error);
      }
    );
  }

  get filteredJugadores() {
    if (this.filtro != "") {
      return this.jugadores.filter(x => (x.user.first_name.toLowerCase() + x.documento + x.user.last_name.toLowerCase()).includes(this.filtro.toLowerCase()));
    }
    return this.jugadores;
  }
  
  async mensajeConfirmacion(id_user: number) {
    const alert = await this.alertController.create({
      header: '¿Enviar invitación?',
      message: 'Le llegará tu invitación y podrá aceptarla o rechazarla',
      buttons: [
        {
          text: 'Cancelar',
          role: 'cancel',
        },
        {
          text: 'OK',
          handler: () => {
            this.enviarInvitacion(id_user);
          },
        },
      ],
    });
    await alert.present();
  }

enviarInvitacion(id_user:number){
  const body ={
    username: this.authService.getUsername(),
    partido: this.id_partido,
    usuario_invitado: id_user
  }
  console.log(body)
  this.invitacionService.invitarUsuario(body).subscribe(
    (data) => {
      this.mensajeExito()
      this.router.navigateByUrl('/home');
      //console.log(data);
    },
    (error: HttpErrorResponse) => {
      this.errorMensaje = error.error[0];
      this.mensajeError(this.errorMensaje)
      //console.log(error.error[0]);
    }  );   
}

async mensajeExito() {
  const alert = await this.alertController.create({
    header: 'Invitacion enviada',
    message: 'Debes esperar la confirmación del usuario.',
    buttons: ['OK'],
  });
  await alert.present();
}
async mensajeError(error:string) {
  const alert = await this.alertController.create({
    header: error,    
    buttons: ['OK'],
  });
  await alert.present();
}

}