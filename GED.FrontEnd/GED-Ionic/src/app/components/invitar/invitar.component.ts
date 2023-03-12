import { Component, OnInit } from '@angular/core';
import { AlertController } from '@ionic/angular';
import { UsuarioService } from 'src/app/services/usuario.service';

@Component({
  selector: 'app-invitar',
  templateUrl: './invitar.component.html',
  styleUrls: ['./invitar.component.scss'],
})
export class InvitarComponent implements OnInit {
  filtro = '';

  jugadores: any[] = [];

  constructor(
    private usuarioService: UsuarioService,
    private alertController: AlertController,
  ) { }

  ngOnInit() {


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

  async mensaje() {
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
          role: 'confirm',
        },
      ],
    });
    await alert.present();
  }
}