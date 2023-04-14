import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { RouteReuseStrategy } from '@angular/router';

import { IonicModule, IonicRouteStrategy } from '@ionic/angular';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './components/home/home.component';
import { LoginComponent } from './components/login/login.component';
import { MisVoucherComponent } from './components/mis-voucher/mis-voucher.component';
import { ProfileComponent } from './components/profile/profile.component';
import { RegisterComponent } from './components/register/register.component';
import { InvitacionesComponent } from './components/invitaciones/invitaciones.component';
import { MisPartidosComponent } from './components/mis-partidos/mis-partidos.component';
import { NuevoPartidoComponent } from './components/nuevo-partido/nuevo-partido.component';
import { ReporteComponent } from './components/reporte/reporte.component';
import { UnirmeComponent } from './components/unirme/unirme.component';
import { InvitarComponent } from './components/invitar/invitar.component';
import { CanjearPuntosComponent } from './components/canjear-puntos/canjear-puntos.component';
import { VoucherComponent } from './components/voucher/voucher.component';
import { ContrasenaComponent } from './components/contrasena/contrasena.component';
import { CommonModule,DatePipe } from '@angular/common';
import { InscriptosPopoverComponent } from './components/inscriptos-popover/inscriptos-popover.component';
import { PartidosSuspendidosComponent } from './components/partidos-suspendidos/partidos-suspendidos.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    RegisterComponent,
    ProfileComponent,
    HomeComponent, 
    MisVoucherComponent, 
    InvitacionesComponent,
    MisPartidosComponent,
    NuevoPartidoComponent,
    ReporteComponent,
    UnirmeComponent,
    InvitarComponent,
    CanjearPuntosComponent,
    VoucherComponent,
    ContrasenaComponent,
    InscriptosPopoverComponent,
    PartidosSuspendidosComponent   
    ],
  imports: [BrowserModule, IonicModule.forRoot(), AppRoutingModule, FormsModule, ReactiveFormsModule,  CommonModule,
    HttpClientModule],
  providers: [{ provide: RouteReuseStrategy, useClass: IonicRouteStrategy },DatePipe],
  bootstrap: [AppComponent],
})
export class AppModule {}
