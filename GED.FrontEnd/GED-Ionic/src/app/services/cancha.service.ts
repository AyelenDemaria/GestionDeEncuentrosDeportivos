import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';


@Injectable({
  providedIn: 'root'
})
export class CanchaService {

  apiUrl = environment.baseURL

  private baseUrl = 'https://ayelend.pythonanywhere.com/canchas/api/';

  constructor(
    private httpClient: HttpClient) { }

  getCanchas(username: string = 'Julieta', password: string = 'Proyecto2022'): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(username + ':' + password)
    });
    return this.httpClient.get<any>('https://ayelend.pythonanywhere.com/canchas/api/', { headers });
  }

  getCanchasByDeporte(body:any, username: string = 'Julieta', password: string = 'Proyecto2022'): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(username + ':' + password)
    });
    const options = { 
      headers: headers,
      body: body
    };
    return this.httpClient.get<any>('https://ayelend.pythonanywhere.com/canchas/api/cancha_deporte', options);
  }

 

//OTRA FORMA PROPORCIONADA POR CHATGPT
  // getCanchasByDeporte(deporte_id: number, username: string = 'Julieta', password: string = 'Proyecto2022'): Observable<any> {
  //   const headers = new HttpHeaders({
  //     'Content-Type': 'application/json',
  //     'Authorization': 'Basic ' + btoa(username + ':' + password)
  //   });
  //   const url = `${this.baseUrl}cancha_deporte/?deporte_id=${deporte_id}`;
  //   return this.httpClient.get<any>(url, { headers }).pipe(
  //     catchError((error: HttpErrorResponse) => {
  //       console.error('Error en la solicitud HTTP:', error);
  //       return throwError('Algo salió mal. Intente de nuevo más tarde.');
  //     })
  //   );
  // }

  // return this.httpClient.get<any>('https://ayelend.pythonanywhere.com/canchas/api/cancha_deporte/',{ headers });
}




