CREATE TABLE `stock_deal_daily` (
  `id` char(10) DEFAULT NULL,
  `start_price` decimal(16,2) DEFAULT NULL,
  `end_price` decimal(16,2) DEFAULT NULL,
  `current_price` decimal(16,2) DEFAULT NULL,
  `highest_price` decimal(16,2) DEFAULT NULL,
  `lowest_price` decimal(16,2) DEFAULT NULL,
  `unit_of_deal` int(16) DEFAULT NULL,
  `amount_of_deal` decimal(20,2) DEFAULT NULL,
  `rdate` char(20) DEFAULT NULL,
  `price_detail_today` char(40) DEFAULT NULL,
  `delta_price_percent` decimal(4,2) DEFAULT NULL,
  `exchange_rate` decimal(4,2) DEFAULT NULL,
  `main_in` decimal(16,2) DEFAULT NULL,
  `main_out` decimal(16,2) DEFAULT NULL,
  `main_in_delta_div_total` decimal(16,2) DEFAULT NULL,
  UNIQUE KEY `stock_date` (`id`,`rdate`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;