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
    this.authService.authenticate(this.form.controls['user'].value,
      this.form.controls['psw'].value).subscribe(x => {
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
