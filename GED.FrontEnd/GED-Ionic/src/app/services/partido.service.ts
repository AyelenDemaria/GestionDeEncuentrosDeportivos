import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class PartidoService {

  apiUrl = environment.baseURL

  constructor(
    private http: HttpClient,
  ) { }

  getPartidos() {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa('Julieta:Proyecto2022')
    });
    return this.http.get<any>('https://ayelend.pythonanywhere.com/partidos/api', { headers: headers })
  }

  postPartido() {
    const body = {
      fechaHora: '',
      cantJugadores: '',
      tipoPartido: '',
      cancha: ''
    }
  }
}
