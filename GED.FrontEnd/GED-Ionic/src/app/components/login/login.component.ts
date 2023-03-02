import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent implements OnInit {
  
  constructor(private fb: FormBuilder, private authService: AuthService) { }
  
  form: FormGroup = this.fb.group({
    email: ['Julieta',Validators.required],
    psw: ['Proyecto2022',Validators.required],
  })

  ngOnInit() {
    this.login();
  }

  login() {
    this.authService.login();
    }



  get email() {
    return this.form.get('email');
  }
  get psw() {
    return this.form.get('psw');
  }
}
