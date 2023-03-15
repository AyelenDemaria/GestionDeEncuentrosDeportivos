import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router} from '@angular/router';
import { UsuarioService } from 'src/app/services/usuario.service';


@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss'],
})
export class RegisterComponent implements OnInit {
 
  
  fecha: string = new Date().toISOString();
  ocultarCalendario = true;
  
  constructor(private fb: FormBuilder, 
              private router: Router,
              private usuarioService: UsuarioService,
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

  crearUsuario() {
      const fechaNacimiento = new Date(this.form.controls['fecha'].value);
      const fechaNacimientoFormateada = fechaNacimiento.toISOString().substring(0, 10);
      const body = {
      username: this.form.controls['user'].value,
      password: this.form.controls['psw'].value,
      nombre: this.form.controls['nombre'].value, 
      apellido: this.form.controls['apellido'].value, 
      documento: Number(this.form.controls['dni'].value),
      telefono: Number(this.form.controls['telefono'].value), 
      fecha_nacimiento: fechaNacimientoFormateada,
      sexo: this.form.controls['sexo'].value,        
    } 
    console.log(body)
    this.usuarioService.postUsuario(body).subscribe(res => console.log(res))
    
  }


}
