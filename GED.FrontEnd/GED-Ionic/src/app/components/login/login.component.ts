import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent implements OnInit {
  
  constructor(private fb: FormBuilder, private authService: AuthService, private router: Router) { }
  
  form: FormGroup = this.fb.group({
    email: ['Julieta',Validators.required],
    psw: ['Proyecto2022',Validators.required],
  })

  ngOnInit() {
    this.login();
  }

  login() {
    this.authService.authenticate(this.form.controls['email'].value, this.form.controls['psw'].value).subscribe(x => {
      this.router.navigateByUrl('/home');
    })
  }

  get email() {
    return this.form.get('email');
  }
  get psw() {
    return this.form.get('psw');
  }
}
