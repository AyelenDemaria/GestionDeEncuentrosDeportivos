import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { AuthService } from './auth.service';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class VoucherService {

  apiUrl = environment.baseURL;

  constructor(private http: HttpClient, private authService: AuthService) { }

  crearVoucher(body: any) {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(this.authService.getUsername() + ':' + this.authService.getPassword())
    });
    return this.http.post<any>(`${this.apiUrl}/vouchers/api`, body, { headers });
  }

  usarVoucher(body: any) {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(this.authService.getUsername() + ':' + this.authService.getPassword())
    });    
    return this.http.put<any>(`${this.apiUrl}/vouchers/api`, body, { headers });
  }

  voucherUser() {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(this.authService.getUsername() + ':' + this.authService.getPassword())
    });
    return this.http.get<any>(`${this.apiUrl}/vouchers/api`, { headers });
  }


  getVoucherById(idVoucher:number): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(this.authService.getUsername() + ':' + this.authService.getPassword()),
    });
    return this.http.get<any>(`${this.apiUrl}/vouchers/api/voucher/?voucher_id=${idVoucher}`, { headers });
  } 



}
