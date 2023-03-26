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
    user: ['', Validators.required],
    psw: ['', Validators.required],
  })

  ngOnInit() {
  
  }

  login() {
    const userValue = this.form.controls['user'].value;
    const userPassword = this.form.controls['psw'].value;
    this.authService.authenticate(userValue, userPassword).subscribe(x => 
      {
        this.router.navigateByUrl('/home');
      })
  }

  get user() {
    return this.form.get('user');
  }
  get psw() {
    return this.form.get('psw');
  }
}
