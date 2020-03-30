-- psql music -a -f country_playlist.sql 
-- Run the file in the music database
-- https://www.postgresql.org/docs/9.5/app-psql.html
-- https://open.spotify.com/playlist/37i9dQZEVXbKfIuOAZrk7G
-- In my country playlist table, the country_code corresponds to the code from my jvectormap & the playlist_id
-- corresponds to the playlist of the country's top 50 songs in spotify.

INSERT INTO country_playlists (country_code, playlist_id)
VALUES 
('GLOBAL', '37i9dQZEVXbLiRSasKsNU9'),
-- United States
('US', '37i9dQZEVXbLRQDuF5jeBp'),
-- United Kingdom
('GB', '37i9dQZEVXbL3DLHfQeDmV'),
-- Andorra
('AD', '37i9dQZEVXbMxjQJh4Um8T'),
-- Argentina
('AR', '37i9dQZEVXbMMy2roB9myp'),
-- Austria
('AT', '37i9dQZEVXbKxYYIUIgn7V'),
-- Australia
('AU', '37i9dQZEVXbO5MSE9RdfN2'),
-- Brazil
('BR', '37i9dQZEVXbMOkSwG072hV'),
-- Belgium
('BE', '197M6xf6aOyCyYijfEe5zM'),
-- Canada
('CA', '37i9dQZEVXbKj23U1GF4IR'),
-- China
('CN', '5MMLA08mEgkMwKz0cSix2S'),
-- France
('FR', '23psvx6vUY6pmJHxE5yagM'),
-- Germany
('DE', '37i9dQZEVXbJiZcmkrIHGU'),
-- Greece
('GR', '37i9dQZEVXbJqdarpmTJDL'),
-- India
('IN', '24ToMDjkwvwWFhXQzrEydv'),
-- Iran
('IR', '6I2Mm0UoSgb1nuF4LbrQYh'),
-- Indonesia
('ID', '37i9dQZEVXbObFQZ3JLcXt'),
-- Italy
('IT', '37i9dQZEVXbKbvcwe5owJ1'),
-- Japan
('JP', '7vVgBVPowZnoZHdQoqB7j3'),
-- Kazakhstan
('KZ', '6dVwWlgvlxfKRVLkZqfFGd'),
-- Mexico
('MX', '37i9dQZEVXbO3qyFxbkOE1'),
-- Norway
('NO', '37i9dQZEVXbJvfa0Yxg7E7'),
-- New Zealand
('NZ', '37i9dQZEVXbM8SIrkERIYl'),
-- Nigeria
('NG', '40wpae7wbObM52hiI92DRw'),
-- Netherlands
('NL', '37i9dQZEVXbKCF6dqVpDkS'),
-- Poland
('PL', '37i9dQZEVXbN6itCcaL3Tt'),
-- Russia
('RU', '2ILlKkIWVmC9u0czMNw3Vp'),
-- South Africa
('ZA', '37i9dQZEVXbNaCk6h5bujZ'),
-- Saudi Arabia
('SA', '5vTptlHUeFynGYqJonU19B'),
-- Spain
('ES', '37i9dQZEVXbNFJfN1Vw8d9'),
-- Switzerland
('CH', '2aJewgqTCoxAsI7D0wJqQS'),
-- Sweden
('SE', '32g1QdVZbo696md2nCP6kF'),
-- South Korea
('KR', '4q2ApZCKGZEqhdVisIdpyL'),
-- Taiwan
('TW', '37i9dQZEVXbMnZEatlMSiu'),
-- Turkey
('TR', '37i9dQZEVXbIVYVBNw9D5K'),
--Thailand
('TH', '37i9dQZEVXbMnz8KIWsvf9'),
--Vietnam
('VN', '0UOuxXm0JMSfn5ESI2NBPo');

