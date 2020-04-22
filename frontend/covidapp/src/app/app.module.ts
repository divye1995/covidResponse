import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';
import { SocialLoginModule, AuthServiceConfig, GoogleLoginProvider } from 'angular4-social-login';
import { ReactiveFormsModule } from '@angular/forms';
import { AgmCoreModule } from '@agm/core';
import { coastConfig } from '../config';

import { AboutComponent } from './about/about.component';
import { LoginComponent } from './user/login/login.component';
import { MatloginComponent } from './user/matlogin/matlogin.component';
import { UserListComponent } from './user/user-list/user-list.component';
import { UserEditComponent } from './user/user-edit/user-edit.component';
import { UserAddComponent } from './user/user-add/user-add.component';
import { RegisterComponent } from './user/register/register.component';
import { RegisterConfirmComponent } from './user/register-confirm/register-confirm.component';
import { PasswordresetComponent } from './user/passwordreset/passwordreset.component';
import { PasswordresetConfirmComponent } from './user/passwordreset-confirm/passwordreset-confirm.component';
import { InviteComponent } from './user/invite/invite.component';
import { ProfileEditComponent } from './user/profile-edit/profile-edit.component';

import { AppComponent } from './app.component';
import { HttpClientModule } from '@angular/common/http';
import { AuthService } from './services/auth.service';
import { DateFilterPipe } from './date-filter.pipe';
import { AvatarEditComponent } from './avatar-edit/avatar-edit.component';
import { TimeFilterPipe } from './time-filter.pipe';
import { PaginatorComponent } from './paginator/paginator.component';
import { Oauth2callbackComponent } from './oauth2callback/oauth2callback.component';
import { CovidCreateComponent } from './covid/covid-create/covid-create.component';
import { ContextCreateComponent } from './context/context-create/context-create.component';
import { ContextFilterComponent } from './context/context-filter/context-filter.component';
import { ContextMapComponent } from './context/context-map/context-map.component';
import { CovidHomeComponent } from './covid/covid-home/covid-home.component';
import { CovidNearbyComponent } from './covid/covid-nearby/covid-nearby.component';
import { CovidLocateComponent } from './covid/covid-locate/covid-locate.component';
import { CovidSearchComponent } from './covid/covid-search/covid-search.component';
import { ContextEditComponent } from './context/context-edit/context-edit.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

// Angular Material
import { MatButtonModule } from '@angular/material';
import { MatCheckboxModule } from '@angular/material';
import { MatCardModule } from '@angular/material/card';
import { MatDialogModule } from "@angular/material";
import { MatExpansionModule } from '@angular/material/expansion';
import { MatToolbarModule } from '@angular/material';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatInputModule} from '@angular/material/input';
import {MatSelectModule} from '@angular/material/select';


// Angular FormIO - https://github.com/formio/angular-formio
import { FormioModule, FormioAppConfig } from 'angular-formio';
import { formioConfig } from './formio/config';
import { FormDisplayComponent } from './formio/form-display/form-display.component';
import { EntitySearchComponent } from './entity/entity-search/entity-search.component';
import { FormCreateComponent } from './formio/form-create/form-create.component';
import { EntityCreateComponent } from './entity/entity-create/entity-create.component';
import { FormEditComponent } from './formio/form-edit/form-edit.component';
import { EntityListComponent } from './entity/entity-list/entity-list.component';
import { EntityEditComponent } from './entity/entity-edit/entity-edit.component';


// Dialogs
import { AddDialogComponent } from './entity/add-dialog/add-dialog.component';
import { EditDialogComponent } from './entity/edit-dialog/edit-dialog.component';
import { MarkerDialogComponent } from './entity/marker-dialog/marker-dialog.component';
import { GmapSearchComponent } from './gmap/gmap-search/gmap-search.component';
import { BulkDialogComponent } from './entity/bulk-dialog/bulk-dialog.component';
import { PrivacyComponent } from './user/privacy/privacy.component';
import { EntityDetailComponent } from './entity/entity-detail/entity-detail.component';
import { AddressSearchComponent } from './gmap/address-search/address-search.component';
import { DashboardComponent } from './entity/dashboard/dashboard.component';


//const google_oauth_client_id:string = '849540517607-9alj6fb3hoo3lhrlml4upqkme070bo2f.apps.googleusercontent.com';

let config = new AuthServiceConfig([
    {
        id: GoogleLoginProvider.PROVIDER_ID,
        provider: new GoogleLoginProvider(coastConfig.GOOGLECLIENTID),
    }
]);

export function provideConfig() {
    return config;
}

@NgModule({
    declarations: [
        AppComponent,
        LoginComponent,
	MatloginComponent,
        ProfileEditComponent,
        DateFilterPipe,
        RegisterComponent,
        UserListComponent,
        UserEditComponent,
        TimeFilterPipe,
        RegisterConfirmComponent,
        AvatarEditComponent,
        PaginatorComponent,
        Oauth2callbackComponent,
        PasswordresetComponent,
        PasswordresetConfirmComponent,
        InviteComponent,
        UserAddComponent,
        CovidCreateComponent,
        ContextCreateComponent,
        ContextFilterComponent,
        ContextMapComponent,
        CovidHomeComponent,
        CovidNearbyComponent,
        CovidLocateComponent,
        CovidSearchComponent,
        ContextEditComponent,
        AboutComponent,
        MarkerDialogComponent,
        FormCreateComponent,
        EntitySearchComponent,
        FormDisplayComponent,
        EntityCreateComponent,
        AddDialogComponent,
        FormEditComponent,
        EntityListComponent,
        EntityEditComponent,
        EditDialogComponent,
        GmapSearchComponent,
        BulkDialogComponent,
        PrivacyComponent,
        EntityDetailComponent,
        AddressSearchComponent,
        DashboardComponent,
    ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        FormsModule,
        FormioModule,
        MatButtonModule,
        MatCardModule,
        MatCheckboxModule,
        MatDialogModule,
	MatSelectModule,
	MatToolbarModule,
        MatExpansionModule,
	MatFormFieldModule,
	MatInputModule,
        ReactiveFormsModule,
        AgmCoreModule.forRoot({
            apiKey: coastConfig.googleAPIKey,
            libraries: ['places']
        }),
        HttpClientModule,
        SocialLoginModule,
        BrowserAnimationsModule
    ],
    providers: [
        AuthService,
        {
            provide: AuthServiceConfig,
            useFactory: provideConfig
        },
	{provide: FormioAppConfig, useValue: formioConfig},
    ],
    bootstrap: [AppComponent],
    entryComponents: [
        AddDialogComponent,
        EditDialogComponent,
        MarkerDialogComponent,
	BulkDialogComponent,
    ]
})
export class AppModule { }
