import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class InscripcionService {

  constructor(
    private http: HttpClient,
  ) { }

  crearInscripcionPartido(body: any) {
    // const headers = new HttpHeaders({
    //   'Content-Type': 'application/json',
    //   'Authorization': 'Basic ' + btoa(username + ':' + password)
    // });
    return this.http.post<any>(`https://ayelend.pythonanywhere.com/inscripciones/api`, body);
  }


  bajaInscripcionPartido(body: string, username: string = 'Julieta', password: string = 'Proyecto2022', inscripcionId) {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(username + ':' + password)
    });
    const options = {
      headers: headers,
      params: body
    }
    return this.http.put<any>('https://ayelend.pythonanywhere.com/inscripciones/api/', options);
  }


  getInscripcionesUser(body:any): Observable<any> {
   
    return this.http.get<any>('https://ayelend.pythonanywhere.com/inscripciones/api/inscripcion/',body);
  }
}