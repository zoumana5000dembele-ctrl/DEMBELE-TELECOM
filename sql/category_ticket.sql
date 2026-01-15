-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Hôte : localhost:3306
-- Généré le : jeu. 15 jan. 2026 à 00:35
-- Version du serveur : 11.4.9-MariaDB-cll-lve
-- Version de PHP : 8.4.16

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";

START TRANSACTION;

SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */
;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */
;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */
;
/*!40101 SET NAMES utf8mb4 */
;

--
-- Base de données : `cp2669223p26_zou-portail-captif`
--

-- --------------------------------------------------------

--
-- Structure de la table `category_ticket`
--

CREATE TABLE `category_ticket` (
    `id` varchar(255) NOT NULL,
    `name` varchar(255) NOT NULL,
    `price` varchar(20) NOT NULL,
    `activity_time` varchar(255) NOT NULL,
    `activity_time_unit` varchar(20) NOT NULL,
    `created_at` datetime NOT NULL
) ENGINE = InnoDB DEFAULT CHARSET = latin1 COLLATE = latin1_swedish_ci;

--
-- Déchargement des données de la table `category_ticket`
--

INSERT INTO
    `category_ticket` (
        `id`,
        `name`,
        `price`,
        `activity_time`,
        `activity_time_unit`,
        `created_at`
    )
VALUES (
        '2',
        'Ticket 500',
        '500 F',
        '6',
        'GO',
        '0000-00-00 00:00:00'
    ),
    (
        '3',
        'Ticket 1000',
        '1000 F',
        '10',
        'GO',
        '0000-00-00 00:00:00'
    ),
    (
        '4',
        'Ticket 1500',
        '1500 F',
        '18',
        'GO',
        '0000-00-00 00:00:00'
    ),
    (
        '5',
        'Ticket 2000',
        '2000 F',
        '25',
        'GO',
        '0000-00-00 00:00:00'
    ),
    (
        '6',
        'Ticket 4000',
        '4000 F',
        '60',
        'GO',
        '0000-00-00 00:00:00'
    );

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `category_ticket`
--
ALTER TABLE `category_ticket` ADD PRIMARY KEY (`id`);

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */
;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */
;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */
;