import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AlertController } from '@ionic/angular';
import { AuthService } from 'src/app/services/auth.service';
import { InvitacionService } from 'src/app/services/invitacion.service';
import { HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'app-invitaciones',
  templateUrl: './invitaciones.component.html',
  styleUrls: ['./invitaciones.component.scss'],
})
export class InvitacionesComponent implements OnInit {

  invitaciones: any[] = []
  errorMensaje:string

  constructor(
    private invitacionesService: InvitacionService,
    private authService: AuthService,
    private router: Router,
    private alertController: AlertController,
  ) { }

  ngOnInit() {
    this.invitacionesService.invitacionesUser().subscribe(
      (data: any[]) => {
        this.invitaciones = data;
        console.log(this.invitaciones);
      },
      (error: any) => {
        console.log(error);
      }
    );
  }

  rechazar(id: number) {
    const body = {
      username: this.authService.getUsername(),
      invitacion_id: id
    }
    console.log(body)
    this.invitacionesService.rechazarInvitacion(body).subscribe(
      (data) => {
        this.mensajeRechazo()
        this.router.navigateByUrl('/invitaciones');
        //console.log(data);
      },
      (error) => {
        console.log(error)
      }
    )
  }

  aceptar(id: number) {
    const body = {
      username: this.authService.getUsername(),
      invitacion_id: id
    }
    console.log(body)
    this.invitacionesService.aceptarInvitacion(body).subscribe(
      (data) => {
        this.mensajeAceptar()
        this.router.navigateByUrl('/invitaciones');
        //console.log(data);
      },
      (error: HttpErrorResponse) => {
        this.errorMensaje = error.error[0];
        this.mensajeError(this.errorMensaje)
        //console.log(error.error[0]);
      }
    )
  }

  async mensajeRechazo() {
    const alert = await this.alertController.create({
      header: 'Invitacion rechazada',
      buttons: ['OK'],
    });
    await alert.present();
  }

  async mensajeAceptar() {
    const alert = await this.alertController.create({
      header: 'Invitacion aceptada',
      buttons: ['OK'],
    });
    await alert.present();
  }

  async mensajeError(error:string) {
    const alert = await this.alertController.create({
      header: error,
      //message: 'Intenta de nuevo más tarde.',
      buttons: ['OK'],
    });
    await alert.present();
  }




}








