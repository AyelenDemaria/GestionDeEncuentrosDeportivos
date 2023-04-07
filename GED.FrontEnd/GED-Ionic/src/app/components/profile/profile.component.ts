import { HttpErrorResponse } from '@angular/common/http';
import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { UsuarioService } from 'src/app/services/usuario.service';
import { AlertController } from '@ionic/angular';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss'],
})
export class ProfileComponent {

  perfil: any;
  telefonoActual: number;
  nuevoTelefono: number;
  mostrarInput:boolean;
  errorMensaje:string;
  

  constructor(
    private usuarioService: UsuarioService,
    private router: Router,
    private alertController: AlertController
    
  ) { }

  ionViewDidEnter() {
    this.perfilUsuario()
    console.log(this.telefonoActual)
  }

  perfilUsuario() {
    this.usuarioService.getDataUsuario().subscribe(
      (data: any[]) => {
        this.perfil = data;
        console.log(this.perfil);
        this.telefonoActual = this.perfil.telefono;
      },
      (error) => {
        console.log(error);
      }
    );
  }

  mostrarInputTelefono() {
    this.mostrarInput = true;
  }


  actualizarTelefono() {
    const body = {
      telefono: this.nuevoTelefono
    };
    this.usuarioService.putUsuario(body).subscribe(
      response => {
        this.telefonoActual = this.nuevoTelefono;
        this.nuevoTelefono = 0;
        this.mostrarInput = false;
      },
      (error: HttpErrorResponse) => {
        if (error.status === 400 && error.error && error.error.telefono) {
          this.errorMensaje = error.error.telefono[0];
        } else {
          this.errorMensaje = "Ha ocurrido un error al actualizar el teléfono.";
        }
        this.mensajeError(this.errorMensaje);
        console.log(error);
      }
    );
  }

  cancelar(){
    this.mostrarInput = false;
    this.router.navigateByUrl('/profile'); 
  }

  contrasena(){    
      this.router.navigateByUrl('/contrasena'); 
    }
  
  
  async mensajeError(error:string) {
    const alert = await this.alertController.create({
      header: error,
      buttons: ['OK'],
    });
    await alert.present();
  }

}
