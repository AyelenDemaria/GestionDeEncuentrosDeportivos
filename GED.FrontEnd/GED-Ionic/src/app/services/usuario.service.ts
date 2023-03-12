import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';


@Injectable({
  providedIn: 'root'
})
export class UsuarioService {
  apiUrl = environment.baseURL

  constructor(
    private http: HttpClient,
  ) { }

  getUsuarios(username: string = 'Julieta', password: string = 'Proyecto2022'): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(username + ':' + password)
    });
    return this.http.get<any>('https://ayelend.pythonanywhere.com/usuarios/api', { headers });
  }

  postUsuario(body: any): Observable<any> {
    // const body = {
    //   username: '',
    //   password: '',
    //   nombre: '', 
    //   apellido: '', 
    //   documento: 0,
    //   telofono: 0, 
    //   fecha_nacimiento: '',
    //   sexo: '',        
    // }
    return this.http.post('https://ayelend.pythonanywhere.com/usuarios/api', body)
  }


  putUsuario(body: any, username: string = 'Julieta', password: string = 'Proyecto2022'): Observable<any> {
    // const body = {
    //   username: '',
    //   password: '',
    //   nombre: '', 
    //   apellido: '', 
    //   documento: 0,
    //   telofono: 0, 
    //   fecha_nacimiento: '',
    //   sexo: '',        
    // }
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(username + ':' + password)
    });
    const options = { 
      headers: headers,
      body: body
    };
    return this.http.put('https://ayelend.pythonanywhere.com/usuarios/api', options)
  }

  putContraseña(body: any, username: string = 'Julieta', password: string = 'Proyecto2022'): Observable<any> {
    // const body = {
    //   password_1: '',
    //   password_2 :''       
    // }
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(username + ':' + password)
    });
    const options = { 
      headers: headers,
      body: body
    };
    return this.http.put('https://ayelend.pythonanywhere.com/usuarios/api/cambiarClave', options)
  }

  getDataUsuario(username: string = 'Julieta', password: string = 'Proyecto2022'): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(username + ':' + password)
    });
    return this.http.get<any>('https://ayelend.pythonanywhere.com/usuarios/api/usuario/', { headers });
  }

  getReporteUsuario(username: string = 'Julieta', password: string = 'Proyecto2022'): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(username + ':' + password)
    });
    return this.http.get<any>('https://ayelend.pythonanywhere.com/usuarios/api/reporteUsuario', { headers });
  }

  getPuntosUsuario(username: string = 'Julieta', password: string = 'Proyecto2022'): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(username + ':' + password)
    });
    return this.http.get<any>('https://ayelend.pythonanywhere.com/usuarios/api/puntosUsuario', { headers });
  }
}





