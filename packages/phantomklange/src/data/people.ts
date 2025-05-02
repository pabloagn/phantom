// packages/phantomklange/src/data/people.ts
// @ts-nocheck

/**
 * Mock database of people/contributors
 */
import { Person } from './types';

export const people: Person[] = [
  {
    id: 'fyodor-dostoyevsky',
    person_id: 'fyodor-dostoyevsky',
    title: 'Fyodor Dostoyevsky',
    slug: 'fyodor-dostoyevsky',
    birth_date: '1821-11-11',
    death_date: '1881-02-09',
    nationality: 'Russian',
    notable_roles: ['Author'],
    description: 'Russian novelist whose works explore human psychology in the troubled political, social, and spiritual atmospheres of 19th-century Russia.',
    excerpt: 'Russian novelist whose works explore human psychology in the troubled political, social, and spiritual atmospheres of 19th-century Russia.',
    content: `<p>Fyodor Mikhailovich Dostoevsky was a Russian novelist, philosopher, short story writer, essayist, and journalist. His literary works explore human psychology in the troubled political, social, and spiritual atmospheres of 19th-century Russia, and engage with a variety of philosophical and religious themes. His most acclaimed novels include Crime and Punishment (1866), The Idiot (1869), Demons (1872), and The Brothers Karamazov (1880).</p>
    <p>Dostoevsky's body of work consists of 12 novels, four novellas, 16 short stories, and numerous other works. Many literary critics rate him as one of the greatest novelists in all of world literature, as multiple of his works are considered to be among the greatest works of literature ever written. His 1864 novella Notes from Underground is considered to be one of the first works of existentialist literature.</p>
    <p>Born in Moscow in 1821, Dostoevsky was introduced to literature at an early age through fairy tales and legends, and through books by Russian and foreign authors. His mother died in 1837 when he was 15, and around the same time, he left school to enter the Nikolayev Military Engineering Institute. After graduating, he worked as an engineer and briefly enjoyed a lavish lifestyle, translating books to earn extra money. In the mid-1840s he wrote his first novel, Poor Folk, which gained him entry into Saint Petersburg's literary circles.</p>`,
    tags: ['literature', 'russia', '19th-century', 'existentialism', 'philosophy', 'psychology'],
    categories: ['Author']
  },
  {
    id: 'andrei-tarkovsky',
    person_id: 'andrei-tarkovsky',
    title: 'Andrei Tarkovsky',
    slug: 'andrei-tarkovsky',
    birth_date: '1932-04-04',
    death_date: '1986-12-29',
    nationality: 'Soviet',
    notable_roles: ['Film Director'],
    description: 'Soviet filmmaker, writer, and film theorist whose poetic and nonlinear films are noted for their spiritual and metaphysical themes.',
    excerpt: 'Soviet filmmaker, writer, and film theorist whose poetic and nonlinear films are noted for their spiritual and metaphysical themes.',
    content: `<p>Andrei Arsenyevich Tarkovsky was a Soviet filmmaker, writer, and film theorist. Widely considered one of the greatest and most influential filmmakers in Soviet and world cinema, his films explored spiritual and metaphysical themes, using a distinctive cinematic style characterized by long takes, dreamlike visual imagery, and metaphorical symbolism.</p>
    <p>Tarkovsky directed seven feature films over his 20-year active career: Ivan's Childhood (1962), Andrei Rublev (1966), Solaris (1972), Mirror (1975), Stalker (1979), Nostalghia (1983), and The Sacrifice (1986). His films were characterized by metaphysical themes, extremely long takes, and memorable images of exceptional visual beauty. Prominent themes in his films include dreams, memory, childhood, running water accompanied by fire, rain indoors, reflections, levitation, and characters re-appearing in the foreground of long panning movements of the camera.</p>
    <p>He directed the first five of his seven feature films in the Soviet Union; his last two films, Nostalghia and The Sacrifice, were produced in Italy and Sweden, respectively. Among his works are Andrei Rublev, Solaris, Mirror, and Stalker. He was a recipient of the Grand Prix du Jury at the Cannes Film Festival (for the film Solaris) and other honors.</p>`,
    tags: ['film', 'soviet cinema', 'director', 'arthouse', 'philosophy'],
    categories: ['Film Director']
  },
  {
    id: 'martin-heidegger',
    person_id: 'martin-heidegger',
    title: 'Martin Heidegger',
    slug: 'martin-heidegger',
    birth_date: '1889-09-26',
    death_date: '1976-05-26',
    nationality: 'German',
    notable_roles: ['Philosopher'],
    description: 'German philosopher whose work is associated with existentialism and phenomenology, exploring the question of Being and authenticity.',
    excerpt: 'German philosopher whose work is associated with existentialism and phenomenology, exploring the question of Being and authenticity.',
    content: `<p>Martin Heidegger was a German philosopher who is widely regarded as one of the most important philosophers of the 20th century. He is best known for his contributions to phenomenology, hermeneutics, and existentialism. His groundbreaking work Being and Time (1927) established his reputation as an original thinker.</p>
    <p>Born in Meßkirch, Germany, Heidegger studied theology before turning to philosophy. He was influenced by Edmund Husserl, who taught him phenomenology. Heidegger later became a professor at the University of Freiburg, where he taught for most of his career. His philosophy explores the question of Being (Sein) and what it means to be human (Dasein).</p>
    <p>Heidegger's work had a profound influence on many fields including philosophy, theology, literary theory, and psychology. His concepts of authenticity, thrownness, and the critique of technology continue to stimulate debate and research in various disciplines. Despite his significant philosophical contributions, his association with Nazism has remained a source of controversy and criticism.</p>`,
    tags: ['philosophy', 'existentialism', 'phenomenology', 'ontology', 'german', '20th-century'],
    categories: ['Philosopher']
  },
  {
    id: 'ingmar-bergman',
    person_id: 'ingmar-bergman',
    title: 'Ingmar Bergman',
    slug: 'ingmar-bergman',
    birth_date: '1918-07-14',
    death_date: '2007-07-30',
    nationality: 'Swedish',
    notable_roles: ['Film Director'],
    description: 'Swedish director, writer, and producer whose films often dealt with existential questions of mortality, loneliness, and faith.',
    excerpt: 'Swedish director, writer, and producer whose films often dealt with existential questions of mortality, loneliness, and faith.',
    content: `<p>Ernst Ingmar Bergman was a Swedish film director, screenwriter, producer, and playwright. Widely considered one of the most accomplished and influential filmmakers of all time, Bergman's films are known for their explorations of mortality, illness, faith, betrayal, and insanity.</p>
    <p>Bergman directed over sixty films and documentaries for cinematic release and for television screenings, most of which he also wrote. He also directed over 170 plays. Among his best-known works are The Seventh Seal (1957), Wild Strawberries (1957), Persona (1966), Cries and Whispers (1972), and Fanny and Alexander (1982).</p>
    <p>Bergman's films usually deal with existential questions of mortality, loneliness, and religious faith. While his earlier films are classified as "chamber dramas," his later work often examines the bleakness of modern life and features characters who are driven to extremes by intense emotional conflicts. Bergman's artistic vision, characterized by intense close-ups and sharp contrasts between light and darkness, has influenced countless filmmakers and artists across different mediums.</p>`,
    tags: ['film', 'swedish cinema', 'director', 'arthouse', 'existentialism'],
    categories: ['Film Director']
  },
  {
    id: 'franz-kafka',
    person_id: 'franz-kafka',
    title: 'Franz Kafka',
    slug: 'franz-kafka',
    birth_date: '1883-07-03',
    death_date: '1924-06-03',
    nationality: 'Czech',
    notable_roles: ['Author'],
    description: 'German-language novelist and short-story writer whose surreal, nightmarish prose explores themes of alienation, existential anxiety, guilt, and absurdity.',
    excerpt: 'German-language novelist and short-story writer whose surreal, nightmarish prose explores themes of alienation, existential anxiety, guilt, and absurdity.',
    content: `<p>Franz Kafka was a German-language novelist and short-story writer, widely regarded as one of the major figures of 20th-century literature. His work fuses elements of realism and the fantastic. It typically features isolated protagonists facing bizarre or surrealistic predicaments and incomprehensible socio-bureaucratic powers.</p>
    <p>Kafka was born into a middle-class German-speaking Jewish family in Prague, the capital of the Kingdom of Bohemia, then part of the Austro-Hungarian Empire, today the capital of the Czech Republic. He trained as a lawyer and after completing his legal education was employed full-time by an insurance company, forcing him to relegate writing to his spare time. Over the course of his life, Kafka wrote hundreds of letters to family and close friends, including his father, with whom he had a strained and formal relationship. He became engaged to several women but never married.</p>
    <p>His best known works include the short story "The Metamorphosis" and novels The Trial and The Castle. These works have influenced a range of writers, critics, artists, and philosophers during the 20th and 21st centuries. In Kafka's fiction, characters struggle with incomprehensible predicaments and surreal scenarios, often involving transformation, isolation, and crushing bureaucracy.</p>`,
    tags: ['literature', 'german', 'surrealism', 'existentialism', 'modernism', 'psychology'],
    categories: ['Author']
  },
  {
    id: 'virginia-woolf',
    person_id: 'virginia-woolf',
    title: 'Virginia Woolf',
    slug: 'virginia-woolf',
    birth_date: '1882-01-25',
    death_date: '1941-03-28',
    nationality: 'British',
    notable_roles: ['Author'],
    description: 'English writer who pioneered the use of stream of consciousness as a narrative device, exploring themes of mental health, gender, and modern society.',
    excerpt: 'English writer who pioneered the use of stream of consciousness as a narrative device, exploring themes of mental health, gender, and modern society.',
    content: `<p>Adeline Virginia Woolf was an English writer, considered one of the most important modernist 20th-century authors and a pioneer in the use of stream of consciousness as a narrative device. Born in London to an affluent household, she was raised by free-thinking parents who encouraged her to read widely from her father's vast library.</p>
    <p>Throughout her life, Woolf was troubled by mental illness. Though she received no formal education, she was tutored in the classics and literature. Together with her husband, Leonard Woolf, she founded the Hogarth Press in 1917, which published works by key modernist writers as well as Woolf's own novels. During the interwar period, she was a significant figure in London literary society and a central figure in the Bloomsbury Group of intellectuals.</p>
    <p>Woolf's works have been translated into more than 50 languages. She is best known for her novels To the Lighthouse, Mrs. Dalloway, and Orlando, and the feminist texts A Room of One's Own and Three Guineas. A pioneer of the modernist movement, she developed a narrative style that focused on psychological depth and employs a blend of memory, perception, and imagination. Her works often explore themes such as mental illness, gender roles, and the impact of social pressures on the individual.</p>`,
    tags: ['literature', 'modernism', 'feminism', 'stream of consciousness', 'british', '20th-century'],
    categories: ['Author']
  },
  {
    id: 'roland-barthes',
    person_id: 'roland-barthes',
    title: 'Roland Barthes',
    slug: 'roland-barthes',
    birth_date: '1915-11-12',
    death_date: '1980-03-26',
    nationality: 'French',
    notable_roles: ['Literary Critic', 'Philosopher'],
    description: 'French literary theorist, philosopher, and semiotician whose work explored numerous fields including structuralism, social theory, and post-structuralism.',
    excerpt: 'French literary theorist, philosopher, and semiotician whose work explored numerous fields including structuralism, social theory, and post-structuralism.',
    content: `<p>Roland Gérard Barthes was a French literary theorist, philosopher, critic, and semiotician. His work engaged in the analysis of a variety of sign systems, mainly derived from Western popular culture. His ideas explored a diverse range of fields and influenced the development of many schools of theory, including structuralism, semiotics, existentialism, Marxism, and post-structuralism.</p>
    <p>Born in Cherbourg, France, Barthes's early life was marked by personal challenges. His father died in a naval battle before his first birthday, and as a young man, he suffered from tuberculosis, which kept him away from academia for several years. Despite these setbacks, he emerged as one of the leading intellectual figures of the 20th century.</p>
    <p>Barthes is perhaps best known for his essay "The Death of the Author" (1967), in which he argued against traditional literary criticism's practice of incorporating the intentions and biographical context of an author in the interpretation of a text. Instead, he emphasized the importance of the reader's interpretation. His book Mythologies (1957) is another influential work, in which he deconstructs the meanings of popular cultural products, revealing the ideological content obscured by their apparent naturalness.</p>`,
    tags: ['literary theory', 'philosophy', 'semiotics', 'structuralism', 'post-structuralism', 'french', '20th-century'],
    categories: ['Literary Critic', 'Philosopher']
  },
  {
    id: 'albert-camus',
    person_id: 'albert-camus',
    title: 'Albert Camus',
    slug: 'albert-camus',
    birth_date: '1913-11-07',
    death_date: '1960-01-04',
    nationality: 'French',
    notable_roles: ['Author', 'Philosopher'],
    description: 'French novelist, essayist, and philosopher known for his philosophy of absurdism and existentialism.',
    excerpt: 'French novelist, essayist, and philosopher known for his philosophy of absurdism and existentialism.',
    content: `<p>Albert Camus was a French philosopher, author, and journalist. He was awarded the 1957 Nobel Prize in Literature at the age of 44, the second-youngest recipient in history. His works include The Stranger, The Plague, The Myth of Sisyphus, The Fall, and The Rebel.</p>
    <p>Camus was born in Algeria to French parents. He grew up in poor conditions, but was a high achiever in school and was admitted to the University of Algiers. However, he contracted tuberculosis in 1930, which forced him to end his studies. This illness also prevented him from taking a teaching position or from joining the military service. Camus was an avid football player until the tuberculosis forced him to stop playing.</p>
    <p>Philosophically, Camus's views contributed to the rise of the philosophy known as absurdism. He is also considered to be an existentialist, even though he firmly rejected the term throughout his lifetime. His philosophy can be understood through his concept of the absurd - the conflict between human tendency to seek inherent value and meaning in life, and the human inability to find any in a purposeless, meaningless, and irrational universe.</p>`,
    tags: ['literature', 'philosophy', 'existentialism', 'absurdism', 'french', '20th-century'],
    categories: ['Author', 'Philosopher']
  },
  {
    id: 'hieronymus-bosch',
    person_id: 'hieronymus-bosch',
    title: 'Hieronymus Bosch',
    slug: 'hieronymus-bosch',
    birth_date: 'c. 1450',
    death_date: 'August 9, 1516',
    nationality: 'Dutch',
    notable_roles: ['painter'],
    description: 'Hieronymus Bosch was a Dutch/Netherlandish painter from Brabant. He is one of the most notable representatives of the Early Netherlandish painting school. His work, generally oil on oak wood, mainly contains fantastic illustrations of religious concepts and narratives. Within his lifetime his work was collected in the Netherlands, Austria, and Spain, and widely copied, especially his macabre and nightmarish depictions of hell.',
    excerpt: 'A visionary painter known for his fantastical and nightmarish depictions of religious themes, particularly his triptych "The Garden of Earthly Delights."',
    poster_image: '/images/people/hieronymus-bosch_poster.jpg',
    cover_image: '/images/people/hieronymus-bosch_cover.jpg',
    tags: ['painter', 'northern renaissance', 'religious art', 'fantasy'],
  },
  {
    id: 'francisco-goya',
    person_id: 'francisco-goya',
    title: 'Francisco Goya',
    slug: 'francisco-goya',
    birth_date: 'March 30, 1746',
    death_date: 'April 16, 1828',
    nationality: 'Spanish',
    notable_roles: ['painter', 'printmaker'],
    description: 'Francisco José de Goya y Lucientes was a Spanish romantic painter and printmaker. He is considered the most important Spanish artist of the late 18th and early 19th centuries. His paintings, drawings, and engravings reflected contemporary historical upheavals and influenced important 19th and 20th century painters. Goya is often referred to as the last of the Old Masters and the first of the moderns.',
    excerpt: 'A Spanish romantic painter and printmaker who documented the dark aspects of Spanish society and produced haunting personal works in his later years.',
    poster_image: '/images/people/francisco-goya_poster.jpg',
    cover_image: '/images/people/francisco-goya_cover.jpg',
    tags: ['painter', 'romanticism', 'printmaker', 'spanish', 'black paintings'],
  },
  {
    id: 'john-everett-millais',
    person_id: 'john-everett-millais',
    title: 'John Everett Millais',
    slug: 'john-everett-millais',
    birth_date: 'June 8, 1829',
    death_date: 'August 13, 1896',
    nationality: 'British',
    notable_roles: ['painter', 'illustrator'],
    description: 'Sir John Everett Millais, 1st Baronet, PRA was an English painter and illustrator who was one of the founders of the Pre-Raphaelite Brotherhood. He was a child prodigy who, aged eleven, became the youngest student to enter the Royal Academy Schools. The Pre-Raphaelite Brotherhood was founded at his family home in London, at 83 Gower Street.',
    excerpt: 'A founding member of the Pre-Raphaelite Brotherhood who created highly detailed, vibrant works inspired by literature and nature.',
    poster_image: '/images/people/john-everett-millais_poster.jpg',
    cover_image: '/images/people/john-everett-millais_cover.jpg',
    tags: ['painter', 'pre-raphaelite', 'victorian', 'british'],
  },
  {
    id: 'henry-fuseli',
    person_id: 'henry-fuseli',
    title: 'Henry Fuseli',
    slug: 'henry-fuseli',
    birth_date: 'February 7, 1741',
    death_date: 'April 17, 1825',
    nationality: 'Swiss',
    notable_roles: ['painter', 'writer'],
    description: 'Henry Fuseli RA was a Swiss painter, draughtsman and writer on art who spent much of his life in Britain. Many of his works, such as The Nightmare, deal with supernatural subject-matter. He painted works for John Boydell\'s Shakespeare Gallery, and created his own "Milton Gallery". He held the post of Professor of Painting at the Royal Academy.',
    excerpt: 'A Swiss-born painter known for his dramatic, imaginative works that explore supernatural themes and the darker aspects of human psychology.',
    poster_image: '/images/people/henry-fuseli_poster.jpg',
    cover_image: '/images/people/henry-fuseli_cover.jpg',
    tags: ['painter', 'romanticism', 'gothic', 'supernatural'],
  },
  {
    id: 'kazimir-malevich',
    person_id: 'kazimir-malevich',
    title: 'Kazimir Malevich',
    slug: 'kazimir-malevich',
    birth_date: 'February 23, 1879',
    death_date: 'May 15, 1935',
    nationality: 'Russian',
    notable_roles: ['painter', 'art theoretician'],
    description: 'Kazimir Severinovich Malevich was a Russian avant-garde artist and art theorist, whose pioneering work and writing had a profound influence on the development of non-objective, or abstract art, in the 20th century. Born in Kiev to an ethnic Polish family, his concept of Suprematism sought to develop a form of expression that moved as far as possible from the world of natural forms and subject matter in order to access "the supremacy of pure feeling" and spirituality.',
    excerpt: 'A pioneering abstract artist who founded the Suprematist movement, believing in the supremacy of pure artistic feeling over representational art.',
    poster_image: '/images/people/kazimir-malevich_poster.jpg',
    cover_image: '/images/people/kazimir-malevich_cover.jpg',
    tags: ['painter', 'suprematism', 'abstract', 'russian', 'avant-garde'],
  },
  {
    id: 'gustav-klimt',
    person_id: 'gustav-klimt',
    title: 'Gustav Klimt',
    slug: 'gustav-klimt',
    birth_date: 'July 14, 1862',
    death_date: 'February 6, 1918',
    nationality: 'Austrian',
    notable_roles: ['painter'],
    description: 'Gustav Klimt was an Austrian symbolist painter and one of the most prominent members of the Vienna Secession movement. Klimt is noted for his paintings, murals, sketches, and other objects d\'art. Klimt\'s primary subject was the female body, and his works are marked by a frank eroticism. His "golden phase" was marked by positive critical reaction and financial success. Many of his paintings from this period include gold leaf.',
    excerpt: 'A symbolist painter and prominent member of the Vienna Secession movement, known for his decorative style and gold leaf technique.',
    poster_image: '/images/people/gustav-klimt_poster.jpg',
    cover_image: '/images/people/gustav-klimt_cover.jpg',
    tags: ['painter', 'symbolism', 'art nouveau', 'vienna secession', 'gold leaf'],
  },
  {
    id: 'andrew-wyeth',
    person_id: 'andrew-wyeth',
    title: 'Andrew Wyeth',
    slug: 'andrew-wyeth',
    birth_date: 'July 12, 1917',
    death_date: 'January 16, 2009',
    nationality: 'American',
    notable_roles: ['painter'],
    description: 'Andrew Newell Wyeth was a visual artist, primarily a realist painter, working predominantly in a regionalist style. He was one of the best-known U.S. artists of the middle 20th century. In his art, Wyeth\'s favorite subjects were the land and people around him, both in his hometown of Chadds Ford, Pennsylvania, and at his summer home in Cushing, Maine.',
    excerpt: 'An American realist painter whose precise, detailed style captured the rural landscapes and people of Pennsylvania and Maine.',
    poster_image: '/images/people/andrew-wyeth_poster.jpg',
    cover_image: '/images/people/andrew-wyeth_cover.jpg',
    tags: ['painter', 'american realism', 'regionalism', 'tempera', 'rural'],
  },
  {
    id: 'theodore-gericault',
    person_id: 'theodore-gericault',
    title: 'Théodore Géricault',
    slug: 'theodore-gericault',
    birth_date: 'September 26, 1791',
    death_date: 'January 26, 1824',
    nationality: 'French',
    notable_roles: ['painter', 'lithographer'],
    description: 'Jean-Louis André Théodore Géricault was a French painter and lithographer, whose best-known painting is The Raft of the Medusa. Although he died young, he was one of the pioneers of the Romantic movement. His dramatic compositions, featuring bold, exotic and often tragic subjects, helped shape French nineteenth-century painting.',
    excerpt: 'A pioneering French Romantic painter whose dramatic compositions explored human emotion and suffering in works like "The Raft of the Medusa."',
    poster_image: '/images/people/theodore-gericault_poster.jpg',
    cover_image: '/images/people/theodore-gericault_cover.jpg',
    tags: ['painter', 'romanticism', 'lithographer', 'historical painting', 'french'],
  },
  {
    id: 'salvador-dali',
    person_id: 'salvador-dali',
    title: 'Salvador Dalí',
    slug: 'salvador-dali',
    birth_date: '1904-05-11',
    death_date: '1989-01-23',
    nationality: 'Spanish',
    notable_roles: ['Painter', 'Sculptor', 'Artist'],
    description: 'Salvador Domingo Felipe Jacinto Dalí i Domènech, Marquess of Dalí of Púbol was a Spanish surrealist artist renowned for his technical skill, precise draftsmanship, and the striking and bizarre images in his work.',
    excerpt: 'A leading proponent of Surrealism known for his striking and bizarre dreamlike imagery, exploring the subconscious mind.',
    content: `<p>Salvador Dalí was a Spanish surrealist artist renowned for his technical skill, precise draftsmanship, and the striking and bizarre images in his work. Born in Figueres, Catalonia, Spain, Dalí was influential among surrealists for his exploration of subconscious imagery.</p>
    <p>His best-known work, The Persistence of Memory, was completed in August 1931, and is one of the most famous Surrealist paintings. Dalí's artistic repertoire included painting, graphic arts, film, sculpture, design and photography, at times in collaboration with other artists. He also wrote fiction, poetry, autobiography, essays and criticism.</p>
    <p>Dalí attributed his "love of everything that is gilded and excessive, my passion for luxury and my love of oriental clothes" to an "Arab lineage", claiming that his ancestors were descended from the Moors. Dalí was highly imaginative, and also enjoyed indulging in unusual and grandiose behavior. His eccentric manner and attention-grabbing public actions sometimes drew more attention than his artwork, to the dismay of those who held his work in high esteem, and to the irritation of his critics.</p>`,
    poster_image: '/images/people/salvador-dali_poster.jpg',
    cover_image: '/images/people/salvador-dali_cover.jpg',
    tags: ['surrealism', 'painting', 'spanish', '20th-century', 'art'],
    categories: ['Artist', 'Painter']
  },
  {
    id: 'vincent-van-gogh',
    person_id: 'vincent-van-gogh',
    title: 'Vincent van Gogh',
    slug: 'vincent-van-gogh',
    birth_date: '1853-03-30',
    death_date: '1890-07-29',
    nationality: 'Dutch',
    notable_roles: ['Painter', 'Artist'],
    description: 'Vincent Willem van Gogh was a Dutch Post-Impressionist painter who posthumously became one of the most famous and influential figures in Western art history.',
    excerpt: 'A Post-Impressionist painter whose expressive brushwork and vivid colors profoundly influenced 20th-century art.',
    content: `<p>Vincent van Gogh was a Dutch post-impressionist painter who is among the most famous and influential figures in the history of Western art. In just over a decade, he created about 2,100 artworks, including around 860 oil paintings, most of which date from the last two years of his life.</p>
    <p>Born into an upper-middle-class family, Van Gogh drew as a child and was serious, quiet, and thoughtful. As a young man, he worked as an art dealer, often traveling, but became depressed after he was transferred to London. He turned to religion and spent time as a Protestant missionary in southern Belgium. He drifted in ill health and solitude before taking up painting in 1881, having moved back home with his parents.</p>
    <p>Van Gogh's early works, mostly still lifes and depictions of peasant laborers, contain few signs of the vivid color that distinguished his later work. In 1886, he moved to Paris, where he met members of the avant-garde, including Émile Bernard and Paul Gauguin, who were reacting against the Impressionist sensibility. As his work developed he created a new approach to still lifes and local landscapes. His paintings grew brighter in color as he developed a style that became fully realized during his stay in Arles in the south of France in 1888.</p>`,
    poster_image: '/images/people/vincent-van-gogh_poster.jpg',
    cover_image: '/images/people/vincent-van-gogh_cover.jpg',
    tags: ['post-impressionism', 'painting', 'dutch', '19th-century', 'art'],
    categories: ['Artist', 'Painter']
  },
  {
    id: 'pablo-picasso',
    person_id: 'pablo-picasso',
    title: 'Pablo Picasso',
    slug: 'pablo-picasso',
    birth_date: '1881-10-25',
    death_date: '1973-04-08',
    nationality: 'Spanish',
    notable_roles: ['Painter', 'Sculptor', 'Artist'],
    description: 'Pablo Ruiz Picasso was a Spanish painter, sculptor, printmaker, ceramicist and theatre designer who spent most of his adult life in France.',
    excerpt: 'A revolutionary Spanish artist who co-founded Cubism and created an extraordinary range of styles and techniques throughout his career.',
    content: `<p>Pablo Picasso was a Spanish painter, sculptor, printmaker, ceramicist and theatre designer who spent most of his adult life in France. Regarded as one of the most influential artists of the 20th century, he is known for co-founding the Cubist movement, the invention of constructed sculpture, the co-invention of collage, and for the wide variety of styles that he helped develop and explore.</p>
    <p>Among his most famous works are the proto-Cubist Les Demoiselles d'Avignon (1907), and the anti-war painting Guernica (1937), a dramatic portrayal of the bombing of Guernica by Nazi Germany's Luftwaffe during the Spanish Civil War.</p>
    <p>Picasso's work is often categorized into periods. While the names of many of his later periods are debated, the most commonly accepted periods in his work are the Blue Period (1901-1904), the Rose Period (1904-1906), the African-influenced Period (1907-1909), Analytic Cubism (1909-1912), and Synthetic Cubism (1912-1919).</p>`,
    poster_image: '/images/people/pablo-picasso_poster.jpg',
    cover_image: '/images/people/pablo-picasso_cover.jpg',
    tags: ['cubism', 'painting', 'sculpture', 'spanish', '20th-century', 'art'],
    categories: ['Artist', 'Painter', 'Sculptor']
  },
  {
    id: 'johannes-vermeer',
    person_id: 'johannes-vermeer',
    title: 'Johannes Vermeer',
    slug: 'johannes-vermeer',
    birth_date: '1632-10-31',
    death_date: '1675-12-15',
    nationality: 'Dutch',
    notable_roles: ['Painter'],
    description: 'Johannes Vermeer was a Dutch Baroque Period painter who specialized in domestic interior scenes of middle-class life.',
    excerpt: 'A master of light and color who specialized in intimate domestic scenes of middle-class Dutch life in the 17th century.',
    content: `<p>Johannes Vermeer was a Dutch Baroque Period painter who specialized in domestic interior scenes of middle-class life. During his lifetime, he was a moderately successful provincial genre painter, recognized in Delft and The Hague. Nonetheless, he produced relatively few paintings and evidently was not wealthy, leaving his wife and children in debt at his death.</p>
    <p>Vermeer worked slowly and with great care, and frequently used very expensive pigments. He is particularly renowned for his masterly treatment and use of light in his work. He painted mostly domestic interior scenes, and most of his paintings are set in the rooms of his house in Delft.</p>
    <p>Recognized during his lifetime in Delft and The Hague, his modest celebrity gave way to obscurity after his death. He was barely mentioned in Arnold Houbraken's major source book on 17th-century Dutch painting (Grand Theatre of Dutch Painters and Women Artists), and was thus omitted from subsequent surveys of Dutch art for nearly two centuries. In the 19th century, Vermeer was rediscovered by Gustav Friedrich Waagen and Théophile Thoré-Bürger, who published an essay attributing 66 pictures to him, although only 34 paintings are universally attributed to him today.</p>`,
    poster_image: '/images/people/johannes-vermeer_poster.jpg',
    cover_image: '/images/people/johannes-vermeer_cover.jpg',
    tags: ['baroque', 'dutch golden age', 'painting', 'dutch', '17th-century', 'art'],
    categories: ['Artist', 'Painter']
  },
  {
    id: 'rembrandt',
    person_id: 'rembrandt',
    title: 'Rembrandt van Rijn',
    slug: 'rembrandt',
    birth_date: '1606-07-15',
    death_date: '1669-10-04',
    nationality: 'Dutch',
    notable_roles: ['Painter', 'Printmaker'],
    description: 'Rembrandt Harmenszoon van Rijn was a Dutch draughtsman, painter, and printmaker. An innovative and prolific master in three media, he is generally considered one of the greatest visual artists in the history of art and the most important in Dutch art history.',
    excerpt: 'A Dutch Golden Age painter renowned for his dramatic use of light and shadow, extraordinary range of emotion, and innovative techniques.',
    content: `<p>Rembrandt Harmenszoon van Rijn was a Dutch draughtsman, painter, and printmaker. An innovative and prolific master in three media, he is generally considered one of the greatest visual artists in the history of art and the most important in Dutch art history.</p>
    <p>Rembrandt's portraits of his contemporaries, self-portraits and illustrations of scenes from the Bible are regarded as his greatest creative triumphs. His self-portraits form a unique and intimate biography, in which the artist surveyed himself without vanity and with the utmost sincerity.</p>
    <p>In his paintings and prints he exhibited knowledge of classical iconography, which he molded to fit the requirements of his own experience; thus, the depiction of a biblical scene was informed by Rembrandt's knowledge of the specific text, his assimilation of classical composition, and his observations of Amsterdam's Jewish population. Because of his empathy for the human condition, he has been called "one of the great prophets of civilization".</p>`,
    poster_image: '/images/people/rembrandt_poster.jpg',
    cover_image: '/images/people/rembrandt_cover.jpg',
    tags: ['baroque', 'dutch golden age', 'painting', 'dutch', '17th-century', 'art'],
    categories: ['Artist', 'Painter']
  },
  {
    id: 'claude-monet',
    person_id: 'claude-monet',
    title: 'Claude Monet',
    slug: 'claude-monet',
    birth_date: '1840-11-14',
    death_date: '1926-12-05',
    nationality: 'French',
    notable_roles: ['Painter'],
    description: 'Oscar-Claude Monet was a French painter and founder of impressionist painting who is seen as a key precursor to modernism, especially in his attempts to paint nature as he perceived it.',
    excerpt: 'A founder of French Impressionism who captured changing light and atmosphere in nature through his distinctive brushwork and color palette.',
    content: `<p>Claude Monet was a French painter, a founder of French Impressionist painting and the most consistent and prolific practitioner of the movement's philosophy of expressing one's perceptions before nature, especially as applied to plein air landscape painting. The term "Impressionism" is derived from the title of his painting Impression, soleil levant (Impression, Sunrise), which was exhibited in 1874 in the first of the independent exhibitions mounted by Monet and his associates as an alternative to the Salon de Paris.</p>
    <p>Born in Paris, France, Monet was raised in Normandy, where his father wanted him to follow his footsteps and go into the family's grocery business. However, Monet wanted to be an artist from a young age, and was encouraged by a local artist, Eugène Boudin, who introduced him to plein air painting and to see the effects of light on color.</p>
    <p>Monet's ambition of documenting the French countryside led him to adopt a method of painting the same scene many times in order to capture the changing of light and the passing of the seasons. From 1883, Monet lived in Giverny, where he purchased a house and property and began a vast landscaping project which included lily ponds that would become the subjects of his best-known works. In 1899 he began painting the water lilies, first in vertical views with a Japanese bridge as a central feature and later in the series of large-scale paintings that was to occupy him continuously for the next 20 years of his life.</p>`,
    poster_image: '/images/people/claude-monet_poster.jpg',
    cover_image: '/images/people/claude-monet_cover.jpg',
    tags: ['impressionism', 'painting', 'french', '19th-century', 'art'],
    categories: ['Artist', 'Painter']
  },
  {
    id: 'sandro-botticelli',
    person_id: 'sandro-botticelli',
    title: 'Sandro Botticelli',
    slug: 'sandro-botticelli',
    birth_date: '1445-03-01',
    death_date: '1510-05-17',
    nationality: 'Italian',
    notable_roles: ['Painter'],
    description: 'Alessandro di Mariano di Vanni Filipepi, known as Sandro Botticelli, was an Italian painter of the Early Renaissance.',
    excerpt: 'An Italian Early Renaissance painter known for his mythological masterpieces and elegant linear style.',
    content: `<p>Alessandro di Mariano di Vanni Filipepi, better known as Sandro Botticelli, was an Italian painter of the Early Renaissance. He belonged to the Florentine School under the patronage of Lorenzo de' Medici, a movement that Giorgio Vasari would characterize less than a hundred years later in his Vita of Botticelli as a "golden age".</p>
    <p>Botticelli's posthumous reputation suffered until the late 19th century; since then, his work has been seen to represent the linear grace of Early Renaissance painting. Among Botticelli's best-known works are The Birth of Venus and Primavera.</p>
    <p>Botticelli lived all his life in the same neighborhood of Florence, with his only significant time elsewhere the months he spent painting in Pisa in 1474 and the Sistine Chapel in Rome in 1481–82. Only one of his paintings is dated (the 1474 Adoration of the Magi), but others can be dated from details of the contemporary background.</p>`,
    poster_image: '/images/people/sandro-botticelli_poster.jpg',
    cover_image: '/images/people/sandro-botticelli_cover.jpg',
    tags: ['renaissance', 'painting', 'italian', '15th-century', 'art'],
    categories: ['Artist', 'Painter']
  },
  {
    id: 'edvard-munch',
    person_id: 'edvard-munch',
    title: 'Edvard Munch',
    slug: 'edvard-munch',
    birth_date: '1863-12-12',
    death_date: '1944-01-23',
    nationality: 'Norwegian',
    notable_roles: ['Painter', 'Printmaker'],
    description: 'Edvard Munch was a Norwegian painter. His best known work, The Scream, has become one of the iconic images of world art.',
    excerpt: 'A Norwegian Expressionist painter whose emotionally charged work explored psychological themes of fear, anxiety, and death.',
    content: `<p>Edvard Munch was a Norwegian painter, whose best known work, The Scream, has become one of the most iconic images of world art. His childhood was overshadowed by illness, bereavement and the dread of inheriting a mental condition that ran in the family. Studying at the Royal School of Art and Design in Kristiania (today's Oslo), Munch began to live a bohemian life under the influence of nihilist Hans Jæger, who urged him to paint his own emotional and psychological state ('soul painting'). From this would develop his distinctive style.</p>
    <p>In the 1890s, Munch traveled to Paris, where he was influenced by the Post-Impressionists. In Berlin, he met Swedish dramatist August Strindberg, whom he painted. As his fame and wealth grew, his emotional state remained insecure. He briefly considered marriage, but could not commit himself. A breakdown in 1908 forced him to give up alcohol. After this, he received many commissions from various patrons, which improved his financial position substantially.</p>
    <p>Munch's works are now represented in numerous major museums and galleries in Norway and abroad. The 1994 version of The Scream was stolen from the National Gallery in Oslo in 1994 and recovered. In 2004, versions of The Scream and Madonna were stolen from the Munch Museum, but recovered in 2006. Munch's The Scream is one of the highest-priced works of art ever sold at auction.</p>`,
    poster_image: '/images/people/edvard-munch_poster.jpg',
    cover_image: '/images/people/edvard-munch_cover.jpg',
    tags: ['expressionism', 'painting', 'norwegian', '19th-century', 'art'],
    categories: ['Artist', 'Painter']
  },
  {
    id: 'diego-velazquez',
    person_id: 'diego-velazquez',
    title: 'Diego Velázquez',
    slug: 'diego-velazquez',
    birth_date: '1599-06-06',
    death_date: '1660-08-06',
    nationality: 'Spanish',
    notable_roles: ['Painter'],
    description: 'Diego Rodríguez de Silva y Velázquez was a Spanish painter, the leading artist in the court of King Philip IV of Spain and Portugal, and one of the most important painters of the Spanish Golden Age.',
    excerpt: 'A Spanish Baroque painter and the leading artist in the court of King Philip IV, known for his masterful technique and influential naturalism.',
    content: `<p>Diego Rodríguez de Silva y Velázquez was a Spanish painter, the leading artist in the court of King Philip IV of Spain and Portugal, and one of the most important painters of the Spanish Golden Age. He was an individualistic artist of the Baroque period. In addition to numerous renditions of scenes of historical and cultural significance, he painted scores of portraits of the Spanish royal family, other notable European figures, and commoners, culminating in the production of his masterpiece Las Meninas (1656).</p>
    <p>From the first quarter of the nineteenth century, Velázquez's artwork was a model for the realist and impressionist painters, in particular Édouard Manet. Since that time, famous modern artists, including Pablo Picasso, Salvador Dalí and Francis Bacon, have paid tribute to Velázquez by recreating several of his most famous works.</p>
    <p>Velázquez was born in Seville, Spain, the first child of Juan Rodriguez de Silva, a notary, and Jerónima Velázquez. His parents belonged to the hidalgo class, the lowest rank of the nobility, which exempted them from taxation. He was educated by his parents to fear God and to develop scholarly habits, but his main interest was in art, and he began his formal artistic training with Francisco Pacheco, a local painter.</p>`,
    poster_image: '/images/people/diego-velazquez_poster.jpg',
    cover_image: '/images/people/diego-velazquez_cover.jpg',
    tags: ['baroque', 'painting', 'spanish', '17th-century', 'art'],
    categories: ['Artist', 'Painter']
  },
  {
    id: 'caspar-david-friedrich',
    person_id: 'caspar-david-friedrich',
    title: 'Caspar David Friedrich',
    slug: 'caspar-david-friedrich',
    birth_date: '1774-09-05',
    death_date: '1840-05-07',
    nationality: 'German',
    notable_roles: ['Painter'],
    description: 'Caspar David Friedrich was a 19th-century German Romantic landscape painter, generally considered the most important German artist of his generation.',
    excerpt: 'A German Romantic landscape painter whose contemplative and symbolic works elevated landscape painting to a spiritual experience.',
    content: `<p>Caspar David Friedrich was a 19th-century German Romantic landscape painter, generally considered the most important German artist of his generation. He is best known for his mid-period allegorical landscapes which typically feature contemplative figures silhouetted against night skies, morning mists, barren trees or Gothic ruins. His primary interest was the contemplation of nature, and his often symbolic and anti-classical work seeks to convey a subjective, emotional response to the natural world.</p>
    <p>Friedrich's paintings deliberately set a human presence in diminished perspective amid expansive landscapes, reducing the figure to a scale that directs the viewer's gaze towards their metaphysical dimension. He was born in the town of Greifswald on the Baltic Sea in what was at that time Swedish Pomerania. He studied in Copenhagen until 1798, before settling in Dresden. His work was recognized for its contemplative aura and often morbid themes.</p>
    <p>Friedrich's work fell into obscurity after his death, but he became a significant figure in German art when the Expressionists and Surrealists rediscovered him in the early 20th century. His most famous works include Wanderer above the Sea of Fog (c. 1818), Abbey in the Oakwood (1810), and The Sea of Ice (1823–24).</p>`,
    poster_image: '/images/people/caspar-david-friedrich_poster.jpg',
    cover_image: '/images/people/caspar-david-friedrich_cover.jpg',
    tags: ['romanticism', 'painting', 'german', '19th-century', 'landscape'],
    categories: ['Artist', 'Painter']
  }
];

/**
 * Utility functions to work with people data
 */

// Get a person by their ID
export const getPersonById = (id: string): Person | undefined => {
  return people.find(person => person.id === id || person.person_id === id);
};

// Get a person by their slug
export const getPersonBySlug = (slug: string): Person | undefined => {
  return people.find(person => person.slug === slug);
};

// Get all people
export const getAllPeople = (): Person[] => {
  return people;
};

// Get people by role
export const getPeopleByRole = (role: string): Person[] => {
  return people.filter(person =>
    person.notable_roles?.includes(role)
  );
};

// Get people by category
export const getPeopleByCategory = (category: string): Person[] => {
  return people.filter(person =>
    person.categories?.includes(category)
  );
};

// Search people by name
export const searchPeopleByName = (query: string): Person[] => {
  const lowercaseQuery = query.toLowerCase();
  return people.filter(person =>
    person.title.toLowerCase().includes(lowercaseQuery)
  );
};

// Search people
export const searchPeople = (query: string): Person[] => {
  const lowercaseQuery = query.toLowerCase();

  return people.filter(person =>
    person.title.toLowerCase().includes(lowercaseQuery) ||
    person.description?.toLowerCase().includes(lowercaseQuery) ||
    person.excerpt?.toLowerCase().includes(lowercaseQuery) ||
    person.nationality?.toLowerCase().includes(lowercaseQuery) ||
    (person.notable_roles && person.notable_roles.some(role =>
      role.toLowerCase().includes(lowercaseQuery)
    ))
  );
};
