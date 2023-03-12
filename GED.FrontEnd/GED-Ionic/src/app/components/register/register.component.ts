import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router} from '@angular/router';
import { CanchaService} from 'src/app/services/cancha.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss'],
})
export class RegisterComponent implements OnInit {
  //private emailPattern: any = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  
  fecha: string = new Date().toISOString();
  ocultarCalendario = true;
  
  constructor(private fb: FormBuilder, 
              private router: Router,
             ) { }  

  public form: FormGroup = this.fb.group({
    nombre: ['', Validators.required],
    apellido: ['', Validators.required],
    edad: ['', [Validators.required, Validators.min(0)]],  
    telefono: ['', [Validators.required, Validators.minLength(7), Validators.min(0)]],
    fecha: ['', Validators.required],
    sexo: ['', Validators.required],
    dni: ['', [Validators.required, Validators.pattern("^[0-9]*$")]],
    user : ['', Validators.required],
    psw: ['', [Validators.required, Validators.minLength(6), Validators.maxLength(15)]],
  })
 
 
  ngOnInit() { 
  
  }

  
  cancel() {
    this.router.navigateByUrl('login')
  }

  get psw() {
    return this.form.get('psw');
  }
  get edad() {
    return this.form.get('edad');
  }
  get telefono() {
    return this.form.get('telefono');
  }
   get user() {
    return this.form.get('user');
  }
  get nombre() {
    return this.form.get('nombre');
  }
  get apellido() {
    return this.form.get('apellido');
  }
  // get fecha() {
  //   return this.form.get('fecha');
  // }
  get sexo() {
    return this.form.get('sexo');
  }
  get dni() {
    return this.form.get('dni');
  }

  abrirCalendario() {
    this.ocultarCalendario = false;
 
  }
  seleccionarFechaHora(evento: any) {
    this.fecha = evento.detail.value;
    console.log(this.fecha); 
  } 



}
