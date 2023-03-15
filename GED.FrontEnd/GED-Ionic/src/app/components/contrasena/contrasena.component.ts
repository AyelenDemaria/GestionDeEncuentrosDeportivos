import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router} from '@angular/router';
import { UsuarioService } from 'src/app/services/usuario.service';

@Component({
  selector: 'app-contrasena',
  templateUrl: './contrasena.component.html',
  styleUrls: ['./contrasena.component.scss'],
})
export class ContrasenaComponent implements OnInit {

  constructor(private fb: FormBuilder, 
    private router: Router,
    private usuarioService: UsuarioService,
   ) { }  

public form: FormGroup = this.fb.group({
psw1: ['', [Validators.required, Validators.minLength(6), Validators.maxLength(15)]],
psw2: ['', [Validators.required, Validators.minLength(6), Validators.maxLength(15)]],
})

  ngOnInit() {}

  cancel() {
    this.router.navigateByUrl('login')
  }

  cambiarContrasena(){
    const body = {
     password_1: this.form.controls['psw1'].value,
     password_2: this.form.controls['psw2'].value,      
    }
    this.usuarioService.putContraseña(body).subscribe(res => console.log(res))
  }

  get psw1() {
    return this.form.get('psw1');
  }

  get psw2() {
      return this.form.get('psw2');
    }
  

}
