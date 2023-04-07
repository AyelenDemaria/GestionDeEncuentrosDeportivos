import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth.service';
import { AlertController } from '@ionic/angular';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent {

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router,
    private alertController: AlertController) { }

  form: FormGroup = this.fb.group({
    user: ['', Validators.required],
    psw: ['', Validators.required],
  })

  login() {
    const userValue = this.form.controls['user'].value;
    const userPassword = this.form.controls['psw'].value;
    this.authService.authenticate(userValue, userPassword).subscribe(
      (data) => { this.form.reset({
        user: '',
        psw: '',     
      });      
        this.router.navigateByUrl('/home');
        //console.log(data);
      },
      (error) => {      
        this.mensajeError()
        //console.log(error.error[0]);
        this.form.reset({
          user: '',
          psw: '',     
        });
      }
    );        
  } 
  get user() {
    return this.form.get('user');
  }
  get psw() {
    return this.form.get('psw');
  }

  async mensajeError() {
    const alert = await this.alertController.create({
      header: 'Usuario o contraseña incorrecta.',
      message: 'Intente de nuevo.',
      buttons: ['OK'],
    });
    await alert.present();
  }
}
