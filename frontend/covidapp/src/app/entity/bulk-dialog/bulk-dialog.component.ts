import { Component, Inject, OnInit, ViewEncapsulation } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from "@angular/material/dialog";
import { FormBuilder, Validators, FormGroup, FormControl } from "@angular/forms";
import { Observable, Subject } from 'rxjs';
import { debounceTime, merge, share, startWith, switchMap } from 'rxjs/operators';

import { formioConfig } from '../../formio/config';
import { UserService } from "../../services/user.service";
import { PublicUser } from "../../models/publicuser";
import { PublicGroup } from "../../models/publicgroup";
import { Page } from '../../pagination';

@Component({
  selector: 'app-bulk-dialog',
  templateUrl: './bulk-dialog.component.html',
  styleUrls: ['./bulk-dialog.component.css']
})
export class BulkDialogComponent implements OnInit {
    form: FormGroup;
    users : any;//Observable<PublicUser[]>;
    groups : any;//Observable<PublicGroup[]>;
    dataLoaded: Promise<boolean>;
    action;
    entities;
    data;
    json_data;
    usergroup;
    form_url:string;
    formioBased:boolean= false;
    assignForm: FormGroup;
    loadVolunteerForm:boolean=false;
    loadGroupForm:boolean=false;
    page: Observable<Page<PublicUser>>;
    pageUrl = new Subject<string>();
    user_role:any;
    groupID:any;
    filterForm: FormGroup;
    statusOptions = [
        {'value': 'to_call', 'name': 'To Call'},
        {'value': 'assign_to_volunteer', 'name': 'Assign To Volunteer'},
        {'value': 'assign_to_org', 'name': 'Assign to Org'},
        {'value': 'followup', 'name': 'Follow Up'},
        {'value': 'closed', 'name': 'Closed'}
    ];

    constructor(
        private fb: FormBuilder,
        private dialogRef: MatDialogRef<BulkDialogComponent>,
        private userService: UserService,
        @Inject(MAT_DIALOG_DATA) data
    ) {
        //console.log(`Inside BulkDialogComponent.constructor(${JSON.stringify(data)})`);
        console.log(`Inside BulkDialogComponent.constructor()`);
        console.log(data);
	this.usergroup = localStorage.getItem('usergroup');
	this.data = data;
        this.action = data.action;
	console.log(this.action);
	if (this.action == "assigntovolunteer"){
		this.formioBased = false;
		this.loadVolunteerForm = true;
	}else if(this.action == "assigntogroup"){
		this.formioBased = false;
		this.loadGroupForm = true;
	}else{
		this.formioBased = true;
	}
	this.entities = data.entities;
	console.log(this.entities);
	this.form_url = formioConfig.appUrl + `/forms/v1/${this.action}`;
	console.log(`Action From URL[${this.form_url}]`);

        this.user_role = localStorage.getItem('ur');
        this.usergroup=localStorage.getItem('usergroup')
            if (this.user_role =="usergroupadmin"){
                this.groupID = "undefined"
            }else{
                this.groupID = localStorage.getItem('groupid');
            }
        this.filterForm = new FormGroup({
          limit : new FormControl(10000),
          formio_usergroup : new FormControl(),
          group__id : new FormControl(this.groupID),
          ordering : new FormControl('name')
        });
        this.page = this.filterForm.valueChanges.pipe(
          debounceTime(200),
          startWith(this.filterForm.value),
          merge(this.pageUrl),
          switchMap(urlOrFilter => this.userService.publicList(urlOrFilter)),
          share()
        );

    }

    ngOnInit() {
	if (this.action == "assigntovolunteer"){
             this.userService.getAllUsersPublic(this.usergroup)
                   .subscribe(
                       data => {
                           console.log(' success', data);
                           this.users = data;
                           this.dataLoaded = Promise.resolve(true);
                       },
                       err => {
                           console.log("Failed");
                           this.dataLoaded = Promise.resolve(false);
                       }
                   );
         }else{
             this.userService.getAllGroupsPublic()
                   .subscribe(
                       data => {
                           console.log(' success', data);
                           this.groups = data;
                           this.dataLoaded = Promise.resolve(true);
                       },
                       err => {
                           console.log("Failed");
                           this.dataLoaded = Promise.resolve(false);
                       }
                   );
	 }


        this.assignForm = new FormGroup({
            assigntovolunteer: new FormControl(),
            assigntogroup: new FormControl(),
        });
        this.form = this.fb.group({
            //description: [this.description, []],
        });
    }

    onSubmit($event) {
        console.log(`Inside add-dialog onSubmit(${$event})`);
        console.log($event.data);
        this.data.json = $event.data;
        this.dialogRef.close(this.data);
    }
    submitAssign(){
        if (this.assignForm.valid) {
             console.log(this.assignForm.value);
             this.data.json = this.assignForm.value;
             this.dialogRef.close(this.data);
	}
    }
    save() {
        this.dialogRef.close(this.form.value);
    }

    close() {
        this.dialogRef.close();
    }
}
