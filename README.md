# Amelia Mae Cosmetics  B2C Ecommerce Website

![Amelia Mae Cosmetics Banner](media/readme-banner.png)

Our website serves both consumers seeking high-quality skincare products from a trusted brand and store owners looking for seamless stock management, article creation, and product management capabilities through the admin login.

## Key Features

- **User Accounts**: Easily create accounts with personal details securely stored.
- **Order History**: Access and review order history for easy reference.
- **Secure Payments**: Make payments securely using Stripe integration.
- **High-Quality Images**: Enjoy high-quality product images for a better shopping experience.
- **Favorites**: Save favorite products for quick access and future purchases.
- **Reviews and Ratings**: Share feedback through reviews and ratings for products.
- **Article Viewing**: Read informative articles on skincare and beauty topics.
- **Admin Control**: Administrators can log in to manage products and articles efficiently.
  - **Product Management**: Create, edit, and delete products easily.
  - **Article Management**: Manage articles with ease, including creation and deletion.
  - **Inventory Tracking**: Track stock sold, lost, and revenue generated.
  - **Stock Management**: Utilize manual and automated processes for stock ordering and receiving.
  - **Inbound Stock Management**: Manage inbound stock deliveries and adjust quantities as needed.

### Website Details

[Git Hub Repo - Amelia Mae Cosmetics](https://github.com/Bowlesy666/amelia-mae-cosmetics)

[Live deployed site - Amelia Mae Cosmetics](https://b2bproject-321684f42c8f.herokuapp.com/)

Want to have a snoop around the admin login functionality? Message me on [my LinkedIn](www.linkedin.com/in/david-bowles-947106216) and i will send over the account details.

Stripe payment system is in development mode, if you wish to try the checkout, please use 4242424242424242...(keep typing 42 till you fill the input box).

___

## Contents

- [Amelia Mae Cosmetics  B2C Ecommerce Website](#amelia-mae-cosmetics--b2c-ecommerce-website)
  - [Key Features](#key-features)
  - [Website Details](#website-details)
  - [Contents](#contents)
  - [UX](#ux)
    - [User Stories](#user-stories)
      - [Target Audience](#target-audience)
      - [Goals](#goals)
      - [Mobile-First Approach](#mobile-first-approach)
  - [Epics \& Their User Stories](#epics--their-user-stories)
      - [User Stories](#user-stories-1)
  - [Design](#design)
    - [WireFrames](#wireframes)
      - [Login/out/404/signup](#loginout404signup)
      - [Base Template Layout](#base-template-layout)
      - [Referrals Dashboard](#referrals-dashboard)
      - [Various layouts](#various-layouts)
    - [Colour Scheme](#colour-scheme)
    - [Imagery](#imagery)
    - [Icons](#icons)
  - [Page Flow](#page-flow)
    - [Multipage Website Design](#multipage-website-design)
      - [Referrals and 1-to-1 Meetings Flow](#referrals-and-1-to-1-meetings-flow)
      - [User Profiles Flow](#user-profiles-flow)
    - [Logo and Title](#logo-and-title)
  - [Features](#features)
    - [General Features](#general-features)
    - [General Features](#general-features-1)
    - [Future Implementations](#future-implementations)
    - [Accessibility](#accessibility)
  - [Technology Used](#technology-used)
    - [Languages Used](#languages-used)
    - [Frameworks, Libraries Packages \& Programs Used](#frameworks-libraries-packages--programs-used)
  - [Deployment and local development](#deployment-and-local-development)
    - [Deployment](#deployment)
      - [Pre-Deployment Tasks](#pre-deployment-tasks)
        - [Hidden Variables](#hidden-variables)
      - [Deploying on Heroku](#deploying-on-heroku)
    - [Local development](#local-development)
      - [Run Locally](#run-locally)
      - [How to clone \& Fork](#how-to-clone--fork)
        - [Clone](#clone)
        - [Fork](#fork)
  - [Testing](#testing)
    - [Validators](#validators)
    - [General Testing](#general-testing)
    - [General Testing](#general-testing-1)
    - [Mobile Testing](#mobile-testing)
    - [Desktop Testing](#desktop-testing)
    - [Bugs](#bugs)
      - [Fixed Bugs](#fixed-bugs)
      - [Unfixed](#unfixed)
      - [Goals](#goals-1)
      - [Testing](#testing-1)
  - [Credits](#credits)

___

## UX

### User Stories

#### Target Audience

The target audience for **Amelia Mae Cosmetics** includes:

- **Skincare Enthusiasts Seeking Quality Products:**
  - Individuals looking for high-quality skincare solutions that deliver results.

- **Luxury Beauty Consumers:**
  - Customers who prioritize luxury and elegance in their skincare routine.

- **Health-Conscious Consumers:**
  - Individuals interested in organic and natural skincare products for sensitive skin.

### Goals

The goals for **Amelia Mae Cosmetics** are:

- **Deliver High-Quality Skincare Solutions:**
  - Provide luxurious skincare products that rejuvenate and nourish the skin effectively.

- **Elevate Skincare Experience with Premium Ingredients:**
  - Offer skincare formulations enriched with premium natural ingredients for optimal results.

- **Empower Users with Expert Advice:**
  - Share expert skincare tips and insights through informative blog posts and articles.

- **Personalized Customer Experience:**
  - Offer personalized recommendations and skincare routines tailored to individual needs.

- **Build Trust and Reliability:**
  - Establish a reputation as a reliable and trustworthy brand in the skincare industry.

### Mobile-First Approach

**Amelia Mae Cosmetics** prioritizes a mobile-first approach to ensure seamless browsing and shopping experiences for users, whether they are at home or on the go.

## Epics & Their User Stories

#### User Stories

Please use drop downs to see user stories.

<details>
  <summary>Epic: Articles</summary>
  <ul>
    <li>As a user, I want to view articles on skincare topics so that I can stay informed and educated about skincare.</li>
    <li>As a user, I want to create articles to share my knowledge and expertise in skincare with others.</li>
    <li>As a user, I want to update articles to ensure that the information provided is accurate and up-to-date.</li>
    <li>As a user, I want to delete articles that are no longer relevant or accurate.</li>
  </ul>
</details>

<details>
  <summary>Epic: Automated Stock Management</summary>
  <ul>
    <li>As a store owner, I want stock levels to be automatically tracked so that I can efficiently manage inventory.</li>
    <li>As a store owner, I want to set reorder thresholds for products to ensure that I never run out of stock.</li>
    <li>As a store owner, I want stock to be automatically replenished when it falls below a certain threshold to avoid stockouts.</li>
    <li>As a store owner, I want to track stock levels to analyze sales trends and forecast future inventory needs.</li>
    <li>As a store owner, I want to log and track referrals for a streamlined process of managing potential revenue opportunities.</li>
    <li>As a store owner, I want to receive email notifications for low stock levels or stock replenishments to stay informed.</li>
    <li>As a store owner, I want to set policies for email notifications and stock management to customize the system according to my preferences.</li>
    <li>As a store owner, I want to automatically generate policies for product returns, refunds, and exchanges to ensure consistency and compliance.</li>
  </ul>
</details>

<details>
  <summary>Epic: Admin Privileges</summary>
  <ul>
    <li>As an admin, I want to add products to the store so that customers have access to a wide range of skincare products.</li>
    <li>As an admin, I want to edit products to update their details or make corrections as needed.</li>
    <li>As an admin, I want to delete products that are discontinued or no longer available for sale.</li>
    <li>As an admin, I want to create, edit, and delete articles to provide valuable content to users and promote engagement.</li>
    <li>As an admin, I want to view user profiles and manage user roles and permissions to ensure platform security and integrity.</li>
    <li>As an admin, I want to generate reports on sales, stock levels, and user activity for data-driven decision-making and business analysis.</li>
  </ul>
</details>

<details>
  <summary>Epic: Wishlist</summary>
  <ul>
    <li>As a user, I want to create a wishlist of skincare products that I'm interested in purchasing in the future.</li>
    <li>As a user, I want to remove items from my wishlist if I change my mind or no longer wish to purchase them.</li>
    <li>As a user, I want to access items from my wishlist directly from my shopping bag for easy checkout.</li>
    <li>As a user, I want to receive email notifications for price drops or promotions on items in my wishlist to take advantage of discounts.</li>
  </ul>
</details>

<details>
  <summary>Epic: Order Placement</summary>
  <ul>
    <li>As a customer, I want to view a summary of my order before finalizing the purchase so that I can review my selections.</li>
    <li>As a customer, I want to input my payment details securely to complete the transaction and make a purchase.</li>
    <li>As a customer, I want to choose shipping details such as shipping address and delivery method to receive my order.</li>
    <li>As a customer, I want to receive a payment confirmation email after successfully placing an order for peace of mind.</li>
    <li>As a customer, I want to track the status of my order and receive updates on its delivery progress for convenience.</li>
  </ul>
</details>

<details>
  <summary>Epic: User Authentication</summary>
  <ul>
    <li>As a user, I want to register for an account to access exclusive features and personalized recommendations.</li>
    <li>As a user, I want to log in to my account securely to view my order history and manage my profile details.</li>
    <li>As a user, I want to update my profile information to keep it accurate and up-to-date.</li>
    <li>As a user, I want to log out of my account to ensure the security of my personal information.</li>
    <li>As a user, I want to receive email notifications for important updates and events, so that I can stay informed and engaged with the platform.</li>
    <li>As a user, I want to be able to update my profile information, so that I can keep my account details accurate and up-to-date.</li>
    <li>As a user, I want the ability to log out of my account securely, so that I can protect my privacy and data.</li>
  </ul>
</details>

<details>
  <summary>Epic: Product Interaction</summary>
  <ul>
    <li>As a user, I want to view detailed product information to make informed decisions about my skincare purchases.</li>
    <li>As a user, I want to search for products by category or keyword to easily find what I'm looking for.</li>
    <li>As a user, I want to add products to my shopping bag and adjust the quantity as needed for a seamless shopping experience.</li>
    <li>As a user, I want to view reviews and ratings from other customers to gauge the effectiveness of skincare products.</li>
    <li>As a user, I want to receive feedback on my shopping bag functionality, so that I can ensure a smooth and intuitive shopping experience.</li>
  </ul>
</details>

___

## Design

### WireFrames

Please see the below for the wireframes and mockups

