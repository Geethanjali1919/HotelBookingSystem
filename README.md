# Hotel Booking System

The **Hotel Booking System** is a cloud-based solution developed using **Flask** and **AWS services** to optimize hotel booking processes for the hospitality industry. This project aims to provide a scalable, efficient, and user-friendly system for managing real-time bookings, availability, and customer notifications. It leverages **AWS DynamoDB** for data management, **S3** for static asset hosting, **SQS** for asynchronous message processing, **SNS** for real-time notifications, and **Lambda** for serverless backend logic. Together, these services enable high availability, seamless event-driven workflows, and dynamic pricing functionality to meet the needs of modern cloud-based systems.

## Technologies Used

- **Flask**: Python framework for backend development.
- **AWS S3**: Hosts static files like HTML, CSS, and JavaScript for a fast, scalable user experience.
- **AWS DynamoDB**: A NoSQL database for storing room, user, and booking information with low-latency access.
- **AWS Lambda**: Serverless functions to handle backend logic, such as availability checks and pricing calculations.
- **AWS SQS**: Manages event-driven booking processes through asynchronous message queues.
- **AWS SNS**: Provides real-time notifications for users via email or SMS.
- **HTML, CSS, JavaScript, Jinja2**: Used for creating an interactive and responsive front-end interface.

## Future Improvements

- Multilingual support
- Payment gateway integration
- Enhanced monitoring with **AWS CloudWatch** to proactively address system performance issues.

The **Hotel Management System** showcases the power of cloud-native design in engineering robust, modern applications for the hospitality domain.

## Installation

To install the project locally:

1. Clone the **Hotel Booking System** repository.
2. Upload the private key to connect the EC2 instance with SSH in the `/.aws/credentials` file.
3. After modifying the credentials, run the following command to start the application:

   ```bash
   $ gunicorn --bind 0.0.0.0:5000 app:app
