import { NgModule } from '@angular/core';
import { PreloadAllModules, RouterModule, Routes } from '@angular/router';
import { AppComponent } from './app.component';
import { CanjearPuntosComponent } from './components/canjear-puntos/canjear-puntos.component';
import { ContrasenaComponent } from './components/contrasena/contrasena.component';
import { HomeComponent } from './components/home/home.component';
import { InvitacionesComponent } from './components/invitaciones/invitaciones.component';
import { InvitarComponent } from './components/invitar/invitar.component';
import { LoginComponent } from './components/login/login.component';
import { MisPartidosComponent } from './components/mis-partidos/mis-partidos.component';
import { MisVoucherComponent } from './components/mis-voucher/mis-voucher.component';
import { NuevoPartidoComponent } from './components/nuevo-partido/nuevo-partido.component';
import { ProfileComponent } from './components/profile/profile.component';
import { RegisterComponent } from './components/register/register.component';
import { ReporteComponent } from './components/reporte/reporte.component';
import { UnirmeComponent } from './components/unirme/unirme.component';
import { VoucherComponent } from './components/voucher/voucher.component';
import { PartidosSuspendidosComponent } from './components/partidos-suspendidos/partidos-suspendidos.component';

const routes: Routes = [
  // {path: 'home' , component: AppComponent},
  {path: '',   redirectTo: '/login', pathMatch: 'full' },
  {path: 'login' , component: LoginComponent},
  {path: 'register', component: RegisterComponent},
  {path: 'profile', component: ProfileComponent},
  {path: 'home', component: HomeComponent},
  {path: 'misVoucher', component: MisVoucherComponent},
  {path: 'invitaciones', component: InvitacionesComponent},
  {path: 'misPartidos', component: MisPartidosComponent},
  {path: 'reporte', component: ReporteComponent},
  {path: 'unirme', component: UnirmeComponent},
  {path: 'nuevoPartido', component: NuevoPartidoComponent},
  {path: 'invitar/:id_partido', component: InvitarComponent},
  {path: 'canjear', component:CanjearPuntosComponent},
  {path: 'voucher/:voucher_id', component:VoucherComponent},
  {path: 'contrasena', component: ContrasenaComponent},
  {path: 'suspendidos', component: PartidosSuspendidosComponent}
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes, { preloadingStrategy: PreloadAllModules })
  ],
  exports: [RouterModule]
})
export class AppRoutingModule {}
