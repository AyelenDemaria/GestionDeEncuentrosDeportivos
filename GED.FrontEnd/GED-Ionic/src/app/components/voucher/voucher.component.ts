import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { VoucherService } from 'src/app/services/voucher.service';
import { Router } from '@angular/router';
import { AlertController } from '@ionic/angular';

@Component({
  selector: 'app-voucher',
  templateUrl: './voucher.component.html',
  styleUrls: ['./voucher.component.scss'],
})
export class VoucherComponent implements OnInit {
  voucher_id: number;
  voucher: any

  constructor(
    private route: ActivatedRoute,
    private VoucherService: VoucherService,
    private router: Router,
    private alertController: AlertController,
  ) { }

  ngOnInit() {

    this.route.params.subscribe(params => {
      this.voucher_id = params['voucher_id']; 
      console.log(this.voucher_id)     
    });

    this.obtenerVoucher(this.voucher_id)
  }


  obtenerVoucher(voucher_id:number){
    this.VoucherService.getVoucherById(voucher_id).subscribe(response => {
      this.voucher = response;
      console.log(response);
    });
  }

  usarVoucher(){
    const body = {
      voucher_id : this.voucher_id
    }
    this.VoucherService.usarVoucher(body).subscribe(
      (data) => {
        this.mensajeExito()
        this.router.navigateByUrl('/home');
        //console.log(data);
      },
      (error) => {
        console.log(error)
      }
    );        
  }

  async mensajeExito() {
    const alert = await this.alertController.create({
      header: 'Voucher usado con éxito!',      
      buttons: ['OK'],
    });
    await alert.present();
  }



 

}
