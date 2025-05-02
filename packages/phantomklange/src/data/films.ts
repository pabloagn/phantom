// packages/phantomklange/src/data/films.ts
// @ts-nocheck

/**
 * Mock database of films
 */
import { Film } from './types';

export const films: Film[] = [
  {
    id: 'stalker',
    film_id: 'stalker',
    title: 'Stalker',
    slug: 'stalker-by-andrei-tarkovsky',
    contributors: [
      { role: 'director', person: 'andrei-tarkovsky' },
      { role: 'screenwriter', person: 'arkady-strugatsky' },
      { role: 'screenwriter', person: 'boris-strugatsky' }
    ],
    release_date: '1979',
    runtime: '162 min',
    country: 'Soviet Union',
    language: 'Russian',
    studio: 'Mosfilm',
    genre: 'Science Fiction',
    description: 'A metaphysical journey through a mysterious "Zone" that contains a room with the supposed ability to fulfill one\'s innermost desires.',
    excerpt: 'A metaphysical journey through a mysterious "Zone" that contains a room with the supposed ability to fulfill one\'s innermost desires.',
    content: `<p>Stalker is a 1979 Soviet science fiction art film directed by Andrei Tarkovsky with a screenplay written by Boris and Arkady Strugatsky, loosely based on their 1972 novel Roadside Picnic. The film combines elements of science fiction with dramatic philosophical and psychological themes.</p>
    <p>The film tells the story of an expedition led by a figure known as the "Stalker" (Alexander Kaidanovsky), who guides his two clients—a melancholic writer (Anatoly Solonitsyn) seeking inspiration, and a professor (Nikolai Grinko) seeking scientific discovery—through a mysterious restricted site known as the "Zone", an area in which the normal laws of reality do not apply and remnants of seemingly extraterrestrial activity lie undisturbed among its ruins.</p>
    <p>The trio's goal is to reach a room at the Zone's center, said to grant the wishes of anyone who steps inside. The Zone is guarded by the police, referred to as "the meat grinder," and entry is restricted and illegal. The area contains various traps and hazards, and the Stalker is needed to navigate them safely.</p>`,
    tags: ['sci-fi', 'art house', 'philosophical', 'soviet cinema', 'post-apocalyptic'],
    categories: ['Science Fiction', 'Art House']
  },
  {
    id: 'mirror',
    film_id: 'mirror',
    title: 'Mirror',
    slug: 'mirror-by-andrei-tarkovsky',
    contributors: [
      { role: 'director', person: 'andrei-tarkovsky' },
      { role: 'screenwriter', person: 'andrei-tarkovsky' }
    ],
    release_date: '1975',
    runtime: '107 min',
    country: 'Soviet Union',
    language: 'Russian',
    studio: 'Mosfilm',
    genre: 'Drama',
    description: 'A poetic and dreamlike film that blends memories, dreams, and newsreels to explore the psychological landscape of a dying poet.',
    excerpt: 'A poetic and dreamlike film that blends memories, dreams, and newsreels to explore the psychological landscape of a dying poet.',
    content: `<p>Mirror is a 1975 Russian art film directed by Andrei Tarkovsky. It is loosely autobiographical, unconventionally structured, and incorporates poems composed and read by the director's father, Arseny Tarkovsky. The film features Margarita Terekhova, Ignat Daniltsev, Alla Demidova, Anatoly Solonitsyn, Tarkovsky's wife Larisa Tarkovskaya, as well as his mother Maria Vishnyakova.</p>
    <p>Mirror is noted for its loose narrative structure, weaving together recollections of childhood, dreams, and wartime newsreels. The film switches between three different time periods: pre-war (1935), war-time (1940s), and post-war (1960s or early '70s), as well as occasional dreams or visions. Mirror draws heavily on Tarkovsky's own childhood, with scenes that recreate memories of his mother, his dacha, and the countryside. The film's cinematography, by Georgy Rerberg, drew on inspiration from Renaissance art, particularly the paintings of Leonardo da Vinci.</p>`,
    tags: ['art house', 'autobiographical', 'non-linear', 'soviet cinema', 'surreal'],
    categories: ['Drama', 'Art House']
  },
  {
    id: 'solaris',
    film_id: 'solaris',
    title: 'Solaris',
    slug: 'solaris-by-andrei-tarkovsky',
    contributors: [
      { role: 'director', person: 'andrei-tarkovsky' },
      { role: 'screenwriter', person: 'andrei-tarkovsky' },
      { role: 'screenwriter', person: 'friedrich-gorenstein' }
    ],
    release_date: '1972',
    runtime: '167 min',
    country: 'Soviet Union',
    language: 'Russian',
    studio: 'Mosfilm',
    genre: 'Science Fiction',
    description: 'A psychological sci-fi drama about a space station orbiting the mysterious planet Solaris, where the crew encounters manifestations of their deepest memories and regrets.',
    excerpt: 'A psychological sci-fi drama about a space station orbiting the mysterious planet Solaris, where the crew encounters manifestations of their deepest memories and regrets.',
    content: `<p>Solaris is a 1972 Soviet science fiction art film based on Stanisław Lem's 1961 novel of the same name. The film was directed by Andrei Tarkovsky and stars Donatas Banionis and Natalya Bondarchuk. The film is a meditative psychological drama occurring mostly aboard a space station orbiting the fictional planet Solaris.</p>
    <p>The scientific mission to the planet Solaris has stalled because the crew of the space station has fallen into separate emotional crises. Psychologist Kris Kelvin travels to the station to evaluate the situation and determine whether the mission should continue. Upon arrival, he finds the station in disarray and the crew behaving oddly. He soon discovers that the planet Solaris is creating physical manifestations of the crew's most painful and repressed memories, including his dead wife, forcing them to confront their past traumas, guilt, and regrets.</p>
    <p>While the novel is about the failure of humans to communicate with a truly alien intelligence, Tarkovsky's adaptation focuses more on the internal human dramas and relationships. The film explores themes of memory, grief, love, and the nature of what it means to be human.</p>`,
    tags: ['sci-fi', 'art house', 'philosophical', 'soviet cinema', 'space'],
    categories: ['Science Fiction', 'Art House']
  },
  {
    id: 'the-seventh-seal',
    film_id: 'the-seventh-seal',
    title: 'The Seventh Seal',
    slug: 'the-seventh-seal-by-ingmar-bergman',
    contributors: [
      { role: 'director', person: 'ingmar-bergman' },
      { role: 'screenwriter', person: 'ingmar-bergman' }
    ],
    release_date: '1957',
    runtime: '96 min',
    country: 'Sweden',
    language: 'Swedish',
    studio: 'Svensk Filmindustri',
    genre: 'Drama',
    description: 'A knight returning from the Crusades encounters Death on a beach and challenges him to a chess match as a means of delaying his fate.',
    excerpt: 'A knight returning from the Crusades encounters Death on a beach and challenges him to a chess match as a means of delaying his fate.',
    content: `<p>The Seventh Seal is a 1957 Swedish historical fantasy film written and directed by Ingmar Bergman. Set in Sweden during the Black Death, it tells of the journey of a medieval knight (Max von Sydow) and a game of chess he plays with the personification of Death (Bengt Ekerot), who has come to take his life.</p>
    <p>The film is considered a classic of world cinema and one of the most influential films of art house cinema. It helped Bergman to establish himself as a world-renowned director and contains scenes which have become iconic through parodies and homages. The title refers to a passage from the Book of Revelation, used both at the very start of the film, and again towards the end, beginning with the words "And when the Lamb had opened the seventh seal, there was silence in heaven about the space of half an hour".</p>`,
    tags: ['medieval', 'existential', 'death', 'religious', 'swedish cinema'],
    categories: ['Drama', 'Art House', 'Historical']
  },
  {
    id: 'persona',
    film_id: 'persona',
    title: 'Persona',
    slug: 'persona-by-ingmar-bergman',
    contributors: [
      { role: 'director', person: 'ingmar-bergman' },
      { role: 'screenwriter', person: 'ingmar-bergman' }
    ],
    release_date: '1966',
    runtime: '83 min',
    country: 'Sweden',
    language: 'Swedish',
    studio: 'Svensk Filmindustri',
    genre: 'Drama',
    description: 'A nurse is put in charge of an actress who has fallen silent after an on-stage breakdown, leading to a strange merging of identities.',
    excerpt: 'A nurse is put in charge of an actress who has fallen silent after an on-stage breakdown, leading to a strange merging of identities.',
    content: `<p>Persona is a 1966 Swedish psychological drama film, written and directed by Ingmar Bergman and starring Bibi Andersson and Liv Ullmann. The film tells the story of a young nurse named Alma (Andersson) and her patient, a famous stage actress named Elisabet Vogler (Ullmann), who has suddenly stopped speaking. They move to a cottage, where Alma cares for Elisabet, confides in her, and begins to have trouble distinguishing herself from her patient.</p>
    <p>Bergman's film explores themes of duality, insanity, identity, and personal crisis. It is notable for its striking imagery, minimal dialogue, and innovative narrative structure. The film is considered one of Bergman's most accomplished works and one of the major artistic achievements of the 1960s.</p>
    <p>Persona is widely regarded as one of the greatest and most influential films in cinema history. It has been the subject of numerous critical analyses and interpretations, with critics and scholars alike drawn to its complex themes, psychological depth, and avant-garde techniques. The film's title comes from the Latin word 'persona,' meaning "mask," which reflects the film's exploration of identity and role-playing.</p>`,
    tags: ['psychological', 'existential', 'identity', 'art house', 'swedish cinema'],
    categories: ['Drama', 'Art House', 'Psychological']
  },
  {
    id: 'tokyo-story',
    film_id: 'tokyo-story',
    title: 'Tokyo Story',
    slug: 'tokyo-story-by-yasujiro-ozu',
    contributors: [
      { role: 'director', person: 'yasujiro-ozu' },
      { role: 'screenwriter', person: 'yasujiro-ozu' },
      { role: 'screenwriter', person: 'kogo-noda' }
    ],
    release_date: '1953',
    runtime: '136 min',
    country: 'Japan',
    language: 'Japanese',
    studio: 'Shochiku',
    genre: 'Drama',
    description: 'An elderly couple journey to Tokyo to visit their grown children, only to be faced with their children\'s indifference.',
    excerpt: 'An elderly couple journey to Tokyo to visit their grown children, only to be faced with their children\'s indifference.',
    content: `<p>Tokyo Story (東京物語, Tōkyō Monogatari) is a 1953 Japanese drama film directed by Yasujirō Ozu and starring Chishū Ryū and Chieko Higashiyama. It tells the story of an aging couple who travel to Tokyo to visit their grown children. The film contrasts the behavior of their children, who are too busy to pay them much attention, with that of their widowed daughter-in-law, who treats them with kindness.</p>
    <p>The film is often regarded as Ozu's masterpiece, and has appeared several times in the British Film Institute's Sight & Sound polls of the greatest films ever made. It is considered to be one of the greatest films of all time, and it is regarded as a masterpiece of Japanese cinema.</p>
    <p>Tokyo Story is a meditation on the relationship between the elderly and their adult children in postwar Japan, exploring themes of family dynamics, generational gaps, and the impact of urbanization on traditional values. Ozu's distinctive style, characterized by low camera positions, minimal movement, and subtle emotional depth, is on full display in this film, creating a contemplative and poignant viewing experience.</p>`,
    tags: ['family', 'japanese cinema', 'post-war', 'generational conflict', 'traditional values'],
    categories: ['Drama', 'Japanese Cinema']
  },
  {
    id: 'late-spring',
    film_id: 'late-spring',
    title: 'Late Spring',
    slug: 'late-spring-by-yasujiro-ozu',
    contributors: [
      { role: 'director', person: 'yasujiro-ozu' },
      { role: 'screenwriter', person: 'yasujiro-ozu' },
      { role: 'screenwriter', person: 'kogo-noda' }
    ],
    release_date: '1949',
    runtime: '108 min',
    country: 'Japan',
    language: 'Japanese',
    studio: 'Shochiku',
    genre: 'Drama',
    description: 'A widower tries to marry off his daughter who is devoted to taking care of him, exploring the tension between tradition and modernity.',
    excerpt: 'A widower tries to marry off his daughter who is devoted to taking care of him, exploring the tension between tradition and modernity.',
    content: `<p>Late Spring (晩春, Banshun) is a 1949 Japanese film directed by Yasujirō Ozu. It is the first installment of Ozu's "Noriko Trilogy," which also includes Early Summer (1951) and Tokyo Story (1953). The film examines the changing dynamics of Japanese society and family life in the post-war era.</p>
    <p>The film centers on the relationship between a widower, Professor Shukichi Somiya (Chishū Ryū), and his twenty-seven-year-old daughter, Noriko (Setsuko Hara), who has devoted her life to caring for her father. Despite Noriko's contentment with her life, her father and her aunt believe it is time for her to marry. The narrative follows their subtle manipulation of Noriko into accepting an arranged marriage, despite her initial resistance.</p>
    <p>Late Spring is celebrated for its sensitive portrayal of the tension between traditional Japanese values and the influence of Western modernization following World War II. The film's quiet, contemplative style and focus on everyday domestic life encapsulates Ozu's signature approach to filmmaking, which often relied on static camera positions, careful composition, and nuanced performances to convey deep emotional resonance.</p>`,
    tags: ['family', 'japanese cinema', 'post-war', 'traditional values', 'father-daughter relationship'],
    categories: ['Drama', 'Japanese Cinema']
  },
  {
    id: 'rashomon',
    film_id: 'rashomon',
    title: 'Rashomon',
    slug: 'rashomon',
    release_date: '1950',
    runtime: '88 minutes',
    country: 'Japan',
    language: 'Japanese',
    studio: 'Daiei Film',
    genre: 'Drama, Crime',
    contributors: [
      { role: 'director', person: 'akira-kurosawa', person_name: 'Akira Kurosawa' },
      { role: 'actor', person: 'toshiro-mifune', person_name: 'Toshirō Mifune' },
      { role: 'actor', person: 'machiko-kyo', person_name: 'Machiko Kyō' },
    ],
    excerpt: 'A heinous crime and its aftermath are recalled from differing points of view, demonstrating the subjective nature of truth.',
    description: 'Rashomon is a 1950 Japanese period psychological thriller film directed by Akira Kurosawa, working in close collaboration with cinematographer Kazuo Miyagawa. The film is based on two stories by Ryūnosuke Akutagawa: "Rashōmon" provides the setting and "In a Grove" provides the characters and plot. The film presents four different accounts of a samurai\'s murder, offering varying perspectives of the same incident. The film is known for its exploration of truth, reality, and the subjective nature of human perceptions.',
    poster_image: '/images/films/rashomon_poster.jpg',
    cover_image: '/images/films/rashomon_cover.jpg',
    tags: ['kurosawa', 'japanese cinema', 'truth', 'perspective', 'crime'],
  },
  {
    id: 'eighth-seal',
    film_id: 'eighth-seal',
    title: 'The Eighth Seal',
    slug: 'the-eighth-seal',
    release_date: '1957',
    runtime: '96 minutes',
    country: 'Sweden',
    language: 'Swedish',
    studio: 'Svensk Filmindustri',
    genre: 'Existential Drama',
    contributors: [
      { role: 'director', person: 'ingmar-bergman', person_name: 'Ingmar Bergman' },
      { role: 'actor', person: 'max-von-sydow', person_name: 'Max von Sydow' },
      { role: 'actor', person: 'gunnar-bjornstrand', person_name: 'Gunnar Björnstrand' },
    ],
    excerpt: 'A knight returning from the Crusades plays a game of chess with Death while seeking answers about life, faith, and God.',
    description: 'The Eighth Seal is a 1957 Swedish historical fantasy film written and directed by Ingmar Bergman. Set in Denmark during the Black Death, it tells the story of a knight (Max von Sydow) who encounters Death, who has come to take him away. The knight challenges Death to a chess match as a means of delaying his inevitable fate, while he tries to commit one meaningful deed in his life. Through the knight and squire\'s journey, the film explores themes of death, existentialism, and the silence of God.',
    poster_image: '/images/films/eighth-seal_poster.jpg',
    cover_image: '/images/films/eighth-seal_cover.jpg',
    tags: ['bergman', 'death', 'existentialism', 'medieval', 'religion'],
  },
  {
    id: 'paris-texas',
    film_id: 'paris-texas',
    title: 'Paris, Texas',
    slug: 'paris-texas',
    release_date: '1984',
    runtime: '145 minutes',
    country: 'West Germany, France, UK, US',
    language: 'English, Spanish',
    studio: 'Road Movies Filmproduktion',
    genre: 'Drama',
    contributors: [
      { role: 'director', person: 'wim-wenders', person_name: 'Wim Wenders' },
      { role: 'actor', person: 'harry-dean-stanton', person_name: 'Harry Dean Stanton' },
      { role: 'actor', person: 'nastassja-kinski', person_name: 'Nastassja Kinski' },
    ],
    excerpt: 'A man wanders out of the desert after a four-year absence and attempts to reconnect with his young son and estranged wife.',
    description: 'Paris, Texas is a 1984 drama film directed by Wim Wenders and starring Harry Dean Stanton, Dean Stockwell, Nastassja Kinski, and Hunter Carson. The screenplay was written by L.M. Kit Carson and playwright Sam Shepard, while the musical score was composed by Ry Cooder. The film tells the story of a man who reunites with his family after disappearing for four years. The film won the Palme d\'Or at the 1984 Cannes Film Festival and is regarded by many critics as one of the greatest films of the 1980s.',
    poster_image: '/images/films/paris-texas_poster.jpg',
    cover_image: '/images/films/paris-texas_cover.jpg',
    tags: ['wenders', 'american west', 'family', 'identity', 'redemption'],
  },
  {
    id: 'au-hasard-balthazar',
    film_id: 'au-hasard-balthazar',
    title: 'Au Hasard Balthazar',
    slug: 'au-hasard-balthazar',
    release_date: '1966',
    runtime: '95 minutes',
    country: 'France',
    language: 'French',
    studio: 'Argos Films',
    genre: 'Drama',
    contributors: [
      { role: 'director', person: 'robert-bresson', person_name: 'Robert Bresson' },
      { role: 'actor', person: 'anne-wiazemsky', person_name: 'Anne Wiazemsky' },
      { role: 'actor', person: 'francois-lafarge', person_name: 'François Lafarge' },
    ],
    excerpt: 'The life of a donkey from birth to death becomes a profound metaphor for human suffering and grace.',
    description: 'Au Hasard Balthazar is a 1966 French drama film directed by Robert Bresson. It follows the life of a donkey named Balthazar as he is passed from owner to owner, experiencing the best and worst of humanity. Through Balthazar, who is both witness to and victim of human behavior, Bresson tells a powerful tale of sin and redemption. The film is known for its austere style and has been praised for its profound spiritual and philosophical themes. Film critic Roger Ebert added the film to his "Great Movies" collection and described it as "the world of Robert Bresson, who believes that everything we need to know about human nature and all the wonder and pity within it can be found in the way we treat the animals in our charge."',
    poster_image: '/images/films/au-hasard-balthazar_poster.jpg',
    cover_image: '/images/films/au-hasard-balthazar_cover.jpg',
    tags: ['bresson', 'donkey', 'suffering', 'french cinema', 'spirituality'],
  },
  {
    id: 'videodrome',
    film_id: 'videodrome',
    title: 'Videodrome',
    slug: 'videodrome',
    release_date: '1983',
    runtime: '87 minutes',
    country: 'Canada',
    language: 'English',
    studio: 'Canadian Film Development Corporation',
    genre: 'Science Fiction, Horror',
    contributors: [
      { role: 'director', person: 'david-cronenberg', person_name: 'David Cronenberg' },
      { role: 'actor', person: 'james-woods', person_name: 'James Woods' },
      { role: 'actor', person: 'debbie-harry', person_name: 'Debbie Harry' },
    ],
    excerpt: 'A television executive discovers a broadcast signal that causes hallucinations and eventually physical transformations.',
    description: 'Videodrome is a 1983 Canadian science fiction body horror film written and directed by David Cronenberg. The film stars James Woods as Max Renn, the CEO of a small TV station who discovers a broadcast signal featuring extreme violence and torture. As he uncovers the signal\'s source, he embarks on a hallucinatory journey that blurs the boundaries between reality and fantasy, ultimately experiencing a series of bizarre and increasingly organic transformations. Videodrome has been described as a prophetic film that anticipated the rise of reality television, the internet, and artificial intelligence.',
    poster_image: '/images/films/videodrome_poster.jpg',
    cover_image: '/images/films/videodrome_cover.jpg',
    tags: ['cronenberg', 'body horror', 'media', 'reality', 'technology'],
  },
  {
    id: 'la-jetee',
    film_id: 'la-jetee',
    title: 'La Jetée',
    slug: 'la-jetee',
    release_date: '1962',
    runtime: '28 minutes',
    country: 'France',
    language: 'French',
    studio: 'Argos Films',
    genre: 'Science Fiction, Short Film',
    contributors: [
      { role: 'director', person: 'chris-marker', person_name: 'Chris Marker' },
      { role: 'actor', person: 'helene-chatelain', person_name: 'Hélène Chatelain' },
      { role: 'actor', person: 'davos-hanich', person_name: 'Davos Hanich' },
    ],
    excerpt: 'A post-apocalyptic story of a man sent back in time to save the future, told almost entirely through still photographs.',
    description: 'La Jetée is a 1962 French science fiction featurette directed by Chris Marker and associated with the Left Bank Cinema movement. Constructed almost entirely from still photos, it tells the story of a post-nuclear war experiment in time travel. A man is sent to the past and future to help mankind rebuild after a devastating war, but becomes fixated on an image from his childhood of a woman on a jetty and a man being killed. The film has been cited as an influence on many subsequent films, notably Terry Gilliam\'s 12 Monkeys (1995), which was a full-length remake of La Jetée.',
    poster_image: '/images/films/la-jetee_poster.jpg',
    cover_image: '/images/films/la-jetee_cover.jpg',
    tags: ['marker', 'time travel', 'still photography', 'post-apocalyptic', 'memory'],
  },
  {
    id: 'seconds',
    film_id: 'seconds',
    title: 'Seconds',
    slug: 'seconds',
    release_date: '1966',
    runtime: '106 minutes',
    country: 'United States',
    language: 'English',
    studio: 'Paramount Pictures',
    genre: 'Science Fiction, Psychological Thriller',
    contributors: [
      { role: 'director', person: 'john-frankenheimer', person_name: 'John Frankenheimer' },
      { role: 'actor', person: 'rock-hudson', person_name: 'Rock Hudson' },
      { role: 'actor', person: 'john-randolph', person_name: 'John Randolph' },
    ],
    excerpt: 'A middle-aged banker is given a second chance at life with a new identity but discovers that rebirth comes at a terrible price.',
    description: 'Seconds is a 1966 American science-fiction drama film directed by John Frankenheimer and starring Rock Hudson. The screenplay by Lewis John Carlino was based on the novel by David Ely. The film tells the story of a middle-aged banker who, dissatisfied with his mundane life, agrees to a process offered by a mysterious company – the "Company" gives wealthy people new identities, and a form of rebirth via plastic surgery. However, he soon discovers that the new life is not what he expected, and the company\'s process is more sinister than it initially appeared. The film addresses themes of alienation, dissatisfaction, and identity crisis.',
    poster_image: '/images/films/seconds_poster.jpg',
    cover_image: '/images/films/seconds_cover.jpg',
    tags: ['frankenheimer', 'identity', 'rebirth', 'dystopia', 'thriller'],
  },
];

/**
 * Utility functions to work with films data
 */

// Get a film by its ID
export const getFilmById = (id: string): Film | undefined => {
  return films.find(film => film.id === id || film.film_id === id);
};

// Get a film by its slug
export const getFilmBySlug = (slug: string): Film | undefined => {
  return films.find(film => film.slug === slug);
};

// Get all films
export const getAllFilms = (): Film[] => {
  return films;
};

// Get films by director (person ID)
export const getFilmsByDirector = (directorId: string): Film[] => {
  return films.filter(film =>
    film.contributors.some(contributor =>
      contributor.role === 'director' && contributor.person === directorId
    )
  );
};

// Get films by country
export const getFilmsByCountry = (country: string): Film[] => {
  return films.filter(film =>
    typeof film.country === 'string'
      ? film.country === country
      : Array.isArray(film.country) && film.country.includes(country)
  );
};

// Get films by genre
export const getFilmsByGenre = (genre: string): Film[] => {
  return films.filter(film => film.genre === genre);
};

// Get films by tag
export const getFilmsByTag = (tag: string): Film[] => {
  return films.filter(film => film.tags?.includes(tag));
};

// Get films by category
export const getFilmsByCategory = (category: string): Film[] => {
  return films.filter(film => film.categories?.includes(category));
};

// Search films by title
export const searchFilmsByTitle = (query: string): Film[] => {
  const lowercaseQuery = query.toLowerCase();
  return films.filter(film =>
    film.title.toLowerCase().includes(lowercaseQuery)
  );
};

// Get latest films
export const getLatestFilms = (count: number = 3): Film[] => {
  return [...films].slice(0, count);
};
