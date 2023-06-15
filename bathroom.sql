-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jun 15, 2023 at 09:19 PM
-- Server version: 10.6.12-MariaDB-0ubuntu0.22.04.1
-- PHP Version: 8.1.2-1ubuntu2.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+08:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `bathroom`
--

-- --------------------------------------------------------

--
-- Table structure for table `bookRooms`
--

CREATE TABLE `bookRooms` (
  `gender` varchar(1) DEFAULT NULL,
  `place` varchar(2) DEFAULT NULL,
  `time` varchar(11) DEFAULT NULL,
  `bookId` int(3) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Catchphase`
--

CREATE TABLE `Catchphase` (
  `id` int(4) NOT NULL,
  `updateTime` varchar(32) NOT NULL,
  `key` varchar(64) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `orderUserList`
--

CREATE TABLE `orderUserList` (
  `realName` varchar(32) DEFAULT NULL,
  `username` varchar(16) DEFAULT NULL,
  `password` varchar(32) DEFAULT NULL,
  `bookstatusid` varchar(8) NOT NULL DEFAULT '0',
  `updateTime` varchar(32) DEFAULT NULL,
  `bathRoomName` varchar(16) DEFAULT NULL,
  `orderTime` varchar(32) DEFAULT NULL,
  `Times` varchar(4) DEFAULT '0',
  `token` varchar(512) DEFAULT 'None',
  `loginid` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Catchphase`
--
ALTER TABLE `Catchphase`
  ADD UNIQUE KEY `updateTime` (`updateTime`);

--
-- Indexes for table `orderUserList`
--
ALTER TABLE `orderUserList`
  ADD UNIQUE KEY `username` (`username`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
