-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Dec 02, 2025 at 01:07 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sports_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin_users`
--

CREATE TABLE `admin_users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `full_name` varchar(100) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `last_login` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `admin_users`
--

INSERT INTO `admin_users` (`id`, `username`, `email`, `password_hash`, `full_name`, `is_active`, `created_at`, `last_login`) VALUES
(1, 'admin', 'admin@example.com', '$2b$12$085Wof5xxJowjyK.wQh34OzOu92M/ezhg89cPUsYHBmGHTW1WLInW', '', 1, '2025-12-02 11:38:18', NULL),
(2, 'admin1', 'admin@gmail.com', '$2b$12$RCov5O6o3VA7BqQFynUwLOZvwMMRYvQjSUhwnhuj1VVgnlnamCQVu', 'admin', 1, '2025-12-02 11:39:53', '2025-12-02 11:40:06'),
(3, 'tashumi', 'tashumi@gmail.com', '$2b$12$MmfqoAWVTQ27.vTYYWt8HOHwseKz7UralRGVAT77uTbtUgC4eME.i', 'tashumi', 1, '2025-12-02 12:06:50', '2025-12-02 12:07:00');

-- --------------------------------------------------------

--
-- Table structure for table `games`
--

CREATE TABLE `games` (
  `id` int(11) NOT NULL,
  `sport` varchar(50) NOT NULL,
  `league` varchar(100) NOT NULL,
  `team1` varchar(100) NOT NULL,
  `team2` varchar(100) NOT NULL,
  `score` varchar(20) NOT NULL,
  `date` date NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `games`
--

INSERT INTO `games` (`id`, `sport`, `league`, `team1`, `team2`, `score`, `date`, `created_at`, `updated_at`) VALUES
(1, 'Soccer', 'Premier League', 'Arsenal', 'Chelsea', '2-1', '2024-01-15', '2025-12-02 10:56:55', '2025-12-02 10:56:55'),
(2, 'Soccer', 'Premier League', 'Liverpool', 'Manchester City', '3-1', '2024-01-16', '2025-12-02 10:56:55', '2025-12-02 10:56:55'),
(3, 'Soccer', 'Premier League', 'Manchester United', 'Tottenham', '1-2', '2024-01-17', '2025-12-02 10:56:55', '2025-12-02 10:56:55'),
(4, 'Soccer', 'La Liga', 'Real Madrid', 'Barcelona', '2-2', '2024-01-18', '2025-12-02 10:56:55', '2025-12-02 10:56:55'),
(5, 'Soccer', 'La Liga', 'Atletico Madrid', 'Sevilla', '3-0', '2024-01-19', '2025-12-02 10:56:55', '2025-12-02 10:56:55'),
(6, 'Soccer', 'Serie A', 'Juventus', 'Inter Milan', '1-0', '2024-01-20', '2025-12-02 10:56:55', '2025-12-02 10:56:55'),
(7, 'Soccer', 'Serie A', 'AC Milan', 'Roma', '2-1', '2024-01-21', '2025-12-02 10:56:55', '2025-12-02 10:56:55'),
(8, 'Soccer', 'Bundesliga', 'Bayern Munich', 'Borussia Dortmund', '4-2', '2024-01-22', '2025-12-02 10:56:55', '2025-12-02 10:56:55'),
(9, 'Basketball', 'NBA', 'Lakers', 'Celtics', '105-98', '2024-01-23', '2025-12-02 10:56:55', '2025-12-02 10:56:55'),
(10, 'Basketball', 'NBA', 'Warriors', 'Bulls', '112-108', '2024-01-24', '2025-12-02 10:56:55', '2025-12-02 10:56:55'),
(11, 'Basketball', 'NBA', 'Heat', 'Spurs', '99-95', '2024-01-25', '2025-12-02 10:56:55', '2025-12-02 10:56:55'),
(12, 'Basketball', 'EuroLeague', 'Real Madrid', 'Barcelona', '89-85', '2024-01-26', '2025-12-02 10:56:55', '2025-12-02 10:56:55'),
(13, 'Basketball', 'EuroLeague', 'Olympiacos', 'Panathinaikos', '78-82', '2024-01-27', '2025-12-02 10:56:55', '2025-12-02 10:56:55'),
(14, 'Basketball', 'College Basketball', 'Duke', 'Kentucky', '78-75', '2024-01-28', '2025-12-02 10:56:55', '2025-12-02 10:56:55'),
(15, 'Basketball', 'College Basketball', 'North Carolina', 'UCLA', '85-80', '2024-01-29', '2025-12-02 10:56:55', '2025-12-02 10:56:55'),
(16, 'Basketball', 'WNBA', 'Las Vegas Aces', 'Seattle Storm', '92-88', '2024-01-30', '2025-12-02 10:56:55', '2025-12-02 10:56:55');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin_users`
--
ALTER TABLE `admin_users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `idx_admin_username` (`username`),
  ADD KEY `idx_admin_email` (`email`);

--
-- Indexes for table `games`
--
ALTER TABLE `games`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_games_date` (`date`),
  ADD KEY `idx_games_sport` (`sport`),
  ADD KEY `idx_games_league` (`league`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin_users`
--
ALTER TABLE `admin_users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `games`
--
ALTER TABLE `games`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
