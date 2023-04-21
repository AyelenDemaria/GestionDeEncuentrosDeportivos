import { Component, OnInit } from '@angular/core';
import { VoucherService } from 'src/app/services/voucher.service';
import { AlertController } from '@ionic/angular';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';


@Component({
  selector: 'app-mis-voucher',
  templateUrl: './mis-voucher.component.html',
  styleUrls: ['./mis-voucher.component.scss'],
})
export class MisVoucherComponent  {
  hoy: Date = new Date();
  vouchers:  any[] = []
  filtro = ''; 

  constructor(
    private voucherService: VoucherService,
    private alertController: AlertController,
    private router: Router
  ) { }

  ionViewDidEnter(){
    console.log(this.hoy);
    // this.vouchers$ = this.voucherService.voucherUser(); 

    this.voucherService.voucherUser().subscribe((data: any[]) => {
      this.vouchers = data;
      console.log(this.vouchers);
    },
    (error) => {
      console.log(error);
    })    
   } 
  

  get filteredVouchers() {
    if (this.filtro != "") {
      return this.vouchers.filter(x => (x.cancha.cancha.nombre.toLowerCase() + x.cancha.valor_uso + x.cancha.valor_referi + x.cancha.cancha.deporte.descripcion.toLowerCase()
        + x.cancha.cancha.direccion.toLowerCase() + x.fecha_emision + x.fecha_vencimiento + x.cancha.valor_uso + x.cancha.valor_referi).
        includes(this.filtro.toLowerCase()));
    }
    return this.vouchers;
  }  

  estadoUsar(canje, venc) {
    const fechaActual = new Date().toISOString().slice(0, 10);
    const rta = canje === undefined || canje === null && venc >= fechaActual;
 
    return (rta)
  }

  estadoVencido(canje, venc){
    const fecha = new Date().toISOString().slice(0, 10);
    const fechaActual = new Date().toISOString().slice(0, 10);
    const rta = canje === undefined || canje === null && venc < fechaActual;

    return (rta)
  }


  usarVoucher(voucher_id: number) {
    setTimeout(() => {
      this.router.navigate(['/voucher', voucher_id]);
    }, 1000); // Espera 1 segundo antes de navegar a la nueva ruta
  }

    //tambien probe estas opciones:
    // this.router.navigate(['/voucher/', voucher_id]);
    // this.router.navigate(['/voucher', voucher_id], {replaceUrl: true})    
    // this.router.navigateByUrl('/voucher/' + voucher_id)

  }


