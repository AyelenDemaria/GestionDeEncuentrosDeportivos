import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router} from '@angular/router';
import { UsuarioService } from 'src/app/services/usuario.service';
import { HttpErrorResponse } from '@angular/common/http';
import { AlertController } from '@ionic/angular';

@Component({
  selector: 'app-contrasena',
  templateUrl: './contrasena.component.html',
  styleUrls: ['./contrasena.component.scss'],
})
export class ContrasenaComponent implements OnInit {
  errorMensaje: string

  constructor(private fb: FormBuilder, 
    private router: Router,
    private usuarioService: UsuarioService,
    private alertController: AlertController,
   ) { }  

public form: FormGroup = this.fb.group({
psw1: ['', [Validators.required, Validators.minLength(6), Validators.maxLength(15)]],
psw2: ['', [Validators.required, Validators.minLength(6), Validators.maxLength(15)]],
})

  ngOnInit() {}

  cancel() {
    this.router.navigateByUrl('profile')
  }

  cambiarContrasena(){
    const body = {
     password_1: this.form.controls['psw1'].value,
     password_2: this.form.controls['psw2'].value,      
    }
    this.usuarioService.putContraseña(body).subscribe(
      (data) => {
        this.mensajeExito()
        this.router.navigateByUrl('/login');
        //console.log(data);
      },
      (error: HttpErrorResponse) => {
        this.errorMensaje = error.error[0];
        this.mensajeError(this.errorMensaje)
        //console.log(error.error[0]);
      }
    );        
  }

  
  async mensajeExito() {
    const alert = await this.alertController.create({
      header: 'Tu contraseña ha sido actualizada',
      message: 'Debes volver a loguearte',
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

  get psw1() {
    return this.form.get('psw1');
  }

  get psw2() {
      return this.form.get('psw2');
  }
  

}
