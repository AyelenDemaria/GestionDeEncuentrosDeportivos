import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  apiUrl = environment.baseURL

  constructor(
    private httpClient: HttpClient,
  ) { }


  login() {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa('Julieta:Proyecto2022')
    });
    this.httpClient.get('https://ayelend.pythonanywhere.com/usuarios/api/login/', { headers: headers })
      .subscribe(data => {
        console.log(data);
      }, error => {
        console.error(error);
      });
  }
}


