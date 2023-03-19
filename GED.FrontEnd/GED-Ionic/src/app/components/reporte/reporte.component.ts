import { Component, OnInit } from '@angular/core';
import { UsuarioService } from 'src/app/services/usuario.service';

@Component({
  selector: 'app-reporte',
  templateUrl: './reporte.component.html',
  styleUrls: ['./reporte.component.scss'],
})
export class ReporteComponent implements OnInit {
  reporte: any[] = []

  constructor(
    private usuarioService: UsuarioService
  ) {

  }

  ngOnInit() {

    const body = {
      username: 'Julieta'
    }
    this.usuarioService.getReporteUsuario(body).subscribe(
      (data: any[]) => {
        this.reporte = data;
        console.log(this.reporte);
      },
      (error: any) => {
        console.log(error);
      }
    );
  }
}
