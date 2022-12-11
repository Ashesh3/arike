Patient Management System in Django

This project is tested with [BrowserStack](https://www.browserstack.com/).

## District Admin

* [x] Profile Page
	- [x] View/Update Profile
	- [x] Change password
 * [x] Facilities Management
	 - [x] List, Create, View, Update, Delete
	 - [x] Filtering + Searching

***Pending***
* [ ] User management without Django Admin Interface

## Nurse (Primary & Secondary)
* [x] Profile Page
	- [x] View/Update Profile
	- [x] Change password
* [x] Patient Management
	* [x] List, Create, View, Update, Delete
	* [x] Searching Patients across any attribute
* [x] Patient Information Management
	* [x] Patient Family Details
		* [x] List, Create, View, Update, Delete Family members
	* [x] Patient Treatment Details
		* [x] List, Create, View, Update, Delete Treatment
		* [x] Treatment Notes on per visitation basis
	* [x] Patient Disease History Details
		* [x] List, Create, View, Update, Delete Disease History

***Pending***
* [ ] Treatment Notes on per visitation basis
* [ ] Email Reports, Visitations and Schedules


## Access control
* [x] User login
* [x] Only `is_verified=True` users are allowed to login
* [x] Access control on each URL endpoint
	* [x] `DistrictAdminAccessMixin`
	* [x] `NurseAccessMixin`

***Pending***
* [ ] More Responsive Design

## Notes
* Access Credentials
	- District Admin
		- **Username**: distadmin
	    - **Password**: distadmin
	-  Primary Nurse
		- **Username**: primarynurse
	    - **Password**: primarynurse
	- Secondary Nurse
		- **Username**: secondarynurse
	    - **Password**: secondarynurse

* Patient named ***Rahmatali Jhah*** contains sample data for Family, Treatment and Disease History.
* Primary Nurse with username `primarynurse` contains sample data for all Patients and is already assigned to a Facility
* District Admin with username `distadmin` contains sample data for Facilities.

## Screenshots
![image](https://user-images.githubusercontent.com/3626859/156928207-8d1f6b48-1026-454b-85c5-31093d8dcbf3.png)

![image](https://user-images.githubusercontent.com/3626859/156928291-63b906ae-8424-4859-bb7e-a84c4ff1590b.png)

![image](https://user-images.githubusercontent.com/3626859/156928302-cff3e1d9-ec21-45cc-a1c6-b75da4ecd994.png)

![image](https://user-images.githubusercontent.com/3626859/156928322-06a0e6a3-6e8e-42df-9c1d-6ca6794c662c.png)

![image](https://user-images.githubusercontent.com/3626859/156928326-88302f17-61ea-4ad0-a1c1-cb594e0880ab.png)

![image](https://user-images.githubusercontent.com/3626859/156928337-ac7fe7ff-3a45-4947-b035-c5ecba8f2fa9.png)

![image](https://user-images.githubusercontent.com/3626859/156928354-de3629e8-54d4-4597-bbf5-e6b570c80344.png)

