import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Http2Server } from 'http2';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class PartidoService {

  apiUrl = environment.baseURL

  constructor(
    private http: HttpClient,
  ) { }

postPartido(){
  const body = {
    fechaHora: '',
    cantJugadores: '',
    tipoPartido: '',
    cancha: ''
  }
  this.http.post(`{apirlUr}/partidos/api`,body)
}
}
