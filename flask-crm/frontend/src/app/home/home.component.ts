import { Component, OnInit } from '@angular/core';
import { User } from '../user';
import { UserService } from '../user.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  users: User[];
  selectedUser: User;

  constructor(private userService: UserService) { }

  ngOnInit(): void {
    this.userService.getUsers()
    .subscribe((data: User[]) => this.users = {...data});
  }

  selectUser(user: User) {
    this.selectedUser = user;
  }


}