import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent implements OnInit {
  
  constructor(private fb: FormBuilder) { }
  
  form: FormGroup = this.fb.group({
    email: ['',Validators.required],
    psw: ['',Validators.required],
  })

  ngOnInit() {}

  async login() {
  }

  get email() {
    return this.form.get('email');
  }
  get psw() {
    return this.form.get('psw');
  }
}
