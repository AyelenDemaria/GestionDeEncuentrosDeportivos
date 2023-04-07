import { Component, OnInit } from '@angular/core';
import { VoucherService } from 'src/app/services/voucher.service';
import { AlertController } from '@ionic/angular';
import { Router } from '@angular/router';


@Component({
  selector: 'app-mis-voucher',
  templateUrl: './mis-voucher.component.html',
  styleUrls: ['./mis-voucher.component.scss'],
})
export class MisVoucherComponent  {
  vouchers: any[] = []
  hoy: Date = new Date();

  constructor(
    private voucherService: VoucherService,
    private alertController: AlertController,
    private router: Router
  ) { }

  ionViewDidEnter(){
    console.log(this.hoy)
    this.voucherService.voucherUser().subscribe(
      (data: any[]) => {
        this.vouchers = data;
        console.log(this.vouchers);
      },
      (error: any) => {
        console.log(error);
      }
    );
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


