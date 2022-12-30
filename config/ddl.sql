CREATE TABLE `users` (
    `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, 
    `created_at` datetime(6) NOT NULL, 
    `updated_at` datetime(6) NOT NULL, 
    `email` varchar(200) NOT NULL UNIQUE, 
    `password` longblob NOT NULL
    )


CREATE TABLE `transactions` (
    `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, 
    `created_at` datetime(6) NOT NULL, 
    `updated_at` datetime(6) NOT NULL, 
    `deposit` integer NOT NULL, 
    `transaction_date` integer NOT NULL, 
    `title` varchar(20) NOT NULL, 
    `description` varchar(100) NOT NULL, 
    `user_id` bigint NOT NULL
    )

 ALTER TABLE `transactions` 
 ADD CONSTRAINT `transactions_user_id_766cc893_fk_users_id` 
 FOREIGN KEY (`user_id`) 
 REFERENCES `users`