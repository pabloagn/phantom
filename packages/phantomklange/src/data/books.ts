// packages/phantomklange/src/data/books.ts
// @ts-nocheck

/**
 * Mock database of books
 */
import { Book } from './types';
import { getPersonById } from './people';

export const books: Book[] = [
  {
    id: 'the-brothers-karamazov',
    book_id: 'the-brothers-karamazov',
    title: 'The Brothers Karamazov',
    slug: 'the-brothers-karamazov-by-fyodor-dostoyevsky',
    contributors: [
      { role: 'author', person: 'fyodor-dostoyevsky' }
    ],
    published_date: '1880',
    description: 'A philosophical novel that explores faith, doubt, and morality through the story of the Karamazov brothers.',
    excerpt: 'A passionate philosophical novel set in 19th-century Russia, exploring faith, doubt, and morality through the story of the Karamazov brothers.',
    content: `<p>The Brothers Karamazov is the final novel by the Russian author Fyodor Dostoevsky, published in 1880. Dostoevsky spent nearly two years writing The Brothers Karamazov, which was completed and published in November 1880. The book is a philosophical novel that enters deeply into the ethical debates of God, free will, and morality. It is a theological drama dealing with problems of faith, doubt, and reason in the context of a modernizing Russia, with a plot that revolves around the subject of patricide. Dostoevsky composed much of the novel in Staraya Russa, which inspired the main setting.</p>
    <p>Since its publication, it has been acclaimed as one of the supreme achievements in world literature. The book portrays a parricide in which each of a murdered man's sons share a varying degree of complicity. The Brothers Karamazov is a passionate philosophical novel set in 19th-century Russia that enters deeply into the ethical debates of God, free will, and morality.</p>`,
    period: '19th Century',
    page_count: 824,
    isbn13: '9780374528379',
    genre: 'Classic Literature',
    publisher: 'The Russian Messenger',
    rating: 5,
    tags: ['russian literature', 'philosophy', 'theological fiction', 'psychological fiction', 'classic'],
    categories: ['Fiction', 'Classic Literature', 'Philosophy']
  },
  {
    id: 'being-and-time',
    book_id: 'being-and-time',
    title: 'Being and Time',
    slug: 'being-and-time-by-martin-heidegger',
    contributors: [
      { role: 'author', person: 'martin-heidegger' }
    ],
    published_date: '1927',
    description: 'A groundbreaking philosophical work examining the concept of Being, temporality, and human existence.',
    excerpt: 'A groundbreaking philosophical work examining the concept of Being, temporality, and human existence.',
    content: `<p>Being and Time is a 1927 book by the German philosopher Martin Heidegger, in which the author seeks to analyse the concept of Being. Heidegger maintains that this has fundamental importance for philosophy and that, since the time of the Ancient Greeks, philosophy has avoided the question, turning instead to the analysis of particular beings.</p>
    <p>The book attempts to revive ontology through an analysis of Dasein, or "being-in-the-world." Heidegger argues that traditional ontology has prejudicially overlooked the question of Being in favor of simply examining specific entities. His project in Being and Time is to uncover the fundamental structures of Being itself, not merely the Being of specific entities.</p>`,
    period: '20th Century',
    page_count: 589,
    isbn13: '9780061575594',
    genre: 'Philosophy',
    publisher: 'SCM Press',
    rating: 4,
    tags: ['philosophy', 'existentialism', 'phenomenology', 'ontology', 'german philosophy'],
    categories: ['Philosophy', 'Non-fiction']
  },
  {
    id: 'crime-and-punishment',
    book_id: 'crime-and-punishment',
    title: 'Crime and Punishment',
    slug: 'crime-and-punishment-by-fyodor-dostoyevsky',
    contributors: [
      { role: 'author', person: 'fyodor-dostoyevsky' }
    ],
    published_date: '1866',
    description: 'A psychological novel that explores the moral dilemmas of a poor ex-student who murders a pawnbroker for her money.',
    excerpt: 'A psychological novel that explores the moral dilemmas of a poor ex-student who murders a pawnbroker for her money.',
    content: `<p>Crime and Punishment focuses on the mental anguish and moral dilemmas of Rodion Raskolnikov, an impoverished ex-student in Saint Petersburg who formulates a plan to kill an unscrupulous pawnbroker for her money. Before the killing, Raskolnikov believes that with the money he could liberate himself from poverty and go on to perform great deeds. However, once it is done he finds himself racked with confusion, paranoia, and disgust for what he has done.</p>
    <p>The novel is often cited as one of the supreme achievements in literature. Crime and Punishment is considered the first great novel of Dostoyevsky's "mature" period of writing. It is the second of his full-length novels after his return from Siberian exile, and the first great Russian philosophical novel, according to some literary critics.</p>`,
    period: '19th Century',
    page_count: 671,
    isbn13: '9780143107637',
    genre: 'Classic Literature',
    publisher: 'The Russian Messenger',
    rating: 5,
    tags: ['russian literature', 'psychological fiction', 'existentialism', 'crime fiction', 'classic'],
    categories: ['Fiction', 'Classic Literature', 'Psychology']
  },
  {
    id: 'notes-from-underground',
    book_id: 'notes-from-underground',
    title: 'Notes from Underground',
    slug: 'notes-from-underground-by-fyodor-dostoyevsky',
    contributors: [
      { role: 'author', person: 'fyodor-dostoyevsky' }
    ],
    published_date: '1864',
    description: 'Considered by many to be one of the first existentialist novels, it presents the diary of a bitter, isolated former civil servant.',
    excerpt: 'Often considered one of the first existentialist works, this novella presents the bitter and alienated thoughts of a nameless narrator isolated from society.',
    content: `<p>Notes from Underground presents itself as an excerpt from the rambling memoirs of a bitter, isolated, unnamed narrator, generally referred to as the Underground Man. The first part of the novel, "Underground", serves as an introduction to the character's unstable and alienated worldview. The second part, "Apropos of the Wet Snow", describes specific events in the narrator's life that shaped his bitter, cynical worldview.</p>
    <p>The novella attacks emerging Western philosophy, especially the notion that humans will naturally act in their own best interests. It also examines the alienation resulting from the narrator's inability to reconcile his individual desires with societal norms and his tendency to overthink and create internal barriers to taking action. The work is considered one of the first existentialist novels and a pioneering work of literary existentialism.</p>`,
    period: '19th Century',
    page_count: 136,
    isbn13: '9780679734529',
    genre: 'Classic Literature',
    publisher: 'Epoch',
    rating: 5,
    tags: ['russian literature', 'existentialism', 'philosophical fiction', 'classic', 'psychological fiction'],
    categories: ['Fiction', 'Classic Literature', 'Philosophy']
  },
  {
    id: 'the-trial',
    book_id: 'the-trial',
    title: 'The Trial',
    slug: 'the-trial-by-franz-kafka',
    contributors: [
      { role: 'author', person: 'franz-kafka' }
    ],
    published_date: '1925',
    description: 'A novel about a man arrested and prosecuted by a remote authority without ever learning the nature of his crime.',
    excerpt: 'A novel about a man arrested and prosecuted by a remote authority without ever learning the nature of his crime.',
    content: `<p>The Trial is a novel written by Franz Kafka between 1914 and 1915 and published posthumously in 1925. One of his best-known works, it tells the story of Josef K., a man arrested and prosecuted by a remote authority without ever learning the nature of his crime. Like Kafka's other novels, The Trial was unfinished at the time of his death, although unlike them it contains a seemingly completed ending.</p>
    <p>The novel's narrative follows Josef K., a chief financial officer at a bank, who is unexpectedly arrested one morning by two unidentified agents for an unspecified crime. The novel progresses through a series of bizarre events as K. attempts to gain access to the mysterious court and understand his case. The book culminates in the execution of K. without any clarification of his purported crime.</p>
    <p>The Trial has been subject to numerous interpretations, with critics analyzing it from various perspectives, including theological, psychoanalytical, sociological, and existentialist. Its depiction of a nightmarish bureaucracy that imposes its will without being understood has resonated with many readers, particularly given the rise of totalitarianism in the 20th century. The novel's exploration of alienation, bureaucracy, and the seemingly relentless miscarriage of justice has solidified its reputation as a quintessentially "Kafkaesque" work.</p>`,
    period: '20th Century',
    page_count: 224,
    isbn13: '9780805209990',
    genre: 'Modern Literature',
    publisher: 'Verlag Die Schmiede',
    rating: 5,
    tags: ['absurdism', 'existentialism', 'surrealism', 'bureaucracy', 'modern fiction', 'german literature'],
    categories: ['Fiction', 'Classic Literature', 'Philosophy']
  },
  {
    id: 'the-metamorphosis',
    book_id: 'the-metamorphosis',
    title: 'The Metamorphosis',
    slug: 'the-metamorphosis-by-franz-kafka',
    contributors: [
      { role: 'author', person: 'franz-kafka' }
    ],
    published_date: '1915',
    description: 'A novella about a man who wakes up one morning to find himself inexplicably transformed into a huge insect.',
    excerpt: 'A novella about a man who wakes up one morning to find himself inexplicably transformed into a huge insect.',
    content: `<p>The Metamorphosis is a novella written by Franz Kafka which was first published in 1915. One of Kafka's best-known works, The Metamorphosis tells the story of salesman Gregor Samsa who wakes one morning to find himself inexplicably transformed into a huge insect (ungeheures Ungeziefer, literally "monstrous vermin"), subsequently struggling to adjust to this new condition.</p>
    <p>The novella explores themes of alienation, existential anxiety, guilt, and identity. Like many of Kafka's works, it has been subject to a wide variety of critical interpretations, incorporating elements of autobiography, and reflecting the influence of a range of literary and philosophical movements, including modernism, magical realism, and existentialism.</p>
    <p>The Metamorphosis begins with Gregor Samsa waking up to find himself transformed into an insect-like creature. The cause of Gregor's transformation is never revealed, and Kafka himself never gave an explanation. The rest of the story deals with Gregor's attempts to adjust to his new condition as he deals with being a burden to his family, who are repulsed by his new form and begin to neglect him. Eventually, Gregor dies, and the story ends with his family seeming to be happier without him.</p>`,
    period: '20th Century',
    page_count: 96,
    isbn13: '9781557427663',
    genre: 'Modern Literature',
    publisher: 'Die Weißen Blätter',
    rating: 5,
    tags: ['absurdism', 'existentialism', 'surrealism', 'body horror', 'modern fiction', 'german literature'],
    categories: ['Fiction', 'Classic Literature', 'Philosophy']
  },
  {
    id: 'to-the-lighthouse',
    book_id: 'to-the-lighthouse',
    title: 'To the Lighthouse',
    slug: 'to-the-lighthouse-by-virginia-woolf',
    contributors: [
      { role: 'author', person: 'virginia-woolf' }
    ],
    published_date: '1927',
    description: 'A landmark novel of high modernism that centers on the Ramsay family and their visits to the Isle of Skye in Scotland between 1910 and 1920.',
    excerpt: 'A landmark novel of high modernism that centers on the Ramsay family and their visits to the Isle of Skye in Scotland between 1910 and 1920.',
    content: `<p>To the Lighthouse is a 1927 novel by Virginia Woolf. The novel is set in the Ramsays' summer house on the Isle of Skye in Scotland, and centers on the Ramsay family's anticipation of and reflection upon a visit to a lighthouse nearby. The novel is divided into three sections: "The Window," "Time Passes," and "The Lighthouse."</p>
    <p>The plot revolves around the Ramsay family's experience at their summer home in the Hebrides, on the Isle of Skye. An expedition to a lighthouse, promised by Mr. Ramsay to his son James but postponed due to bad weather, serves as the connecting thread of the narrative. The novel explores themes of perception, time, and the nature of reality, as Woolf employs her distinctive stream-of-consciousness style to delve into her characters' thoughts, emotions, and memories.</p>
    <p>To the Lighthouse is widely regarded as one of Woolf's most successful and accessible works. It showcases her innovative narrative techniques and her focus on the fluidity of time and the complexity of human relationships. The novel is a deeply personal work for Woolf, drawing on her own childhood experiences and serving as a tribute to her parents. Its exploration of gender roles, especially in relation to artistry and domestic life, has made it a significant text in feminist literary criticism.</p>`,
    period: '20th Century',
    page_count: 209,
    isbn13: '9780156907392',
    genre: 'Modern Literature',
    publisher: 'Hogarth Press',
    rating: 5,
    tags: ['modernism', 'stream of consciousness', 'british literature', 'feminist literature', 'psychological fiction'],
    categories: ['Fiction', 'Classic Literature', 'Modernism']
  },
  {
    id: 'the-waves',
    book_id: 'the-waves',
    title: 'The Waves',
    slug: 'the-waves-by-virginia-woolf',
    contributors: [
      { role: 'author', person: 'virginia-woolf' }
    ],
    published_date: '1931',
    description: 'An experimental novel that follows the lives of six characters from childhood to adulthood through a series of soliloquies.',
    excerpt: 'An experimental novel that follows the lives of six characters from childhood to adulthood through a series of soliloquies.',
    content: `<p>The Waves is an experimental novel by Virginia Woolf, published in 1931. It is considered her most experimental work, and consists of soliloquies spoken by the book's six characters: Bernard, Susan, Rhoda, Neville, Jinny, and Louis. Also important is Percival, the seventh character, who never speaks but is the subject of frequent reflection by the others. The soliloquies that span the characters' lives are broken up by nine brief third-person interludes detailing a coastal scene at varying stages in a day from sunrise to sunset.</p>
    <p>The novel is written in a highly poetic style, with vivid imagery and lyrical language. Each character has a distinct perspective and voice, which Woolf uses to explore themes of identity, perception, and the passage of time. The work is often described as a "play-poem" or "playpoem," reflecting its unique blend of poetic and dramatic elements.</p>
    <p>The Waves follows the characters from childhood to old age, revealing their evolving relationships with each other and their internal struggles with self-identity. The death of Percival, a charismatic figure whom all the characters admire, serves as a pivotal event in the narrative. Through these characters' reflections, Woolf examines universal questions about the nature of existence, the search for meaning, and the impact of death on the living.</p>`,
    period: '20th Century',
    page_count: 248,
    isbn13: '9780156949606',
    genre: 'Modern Literature',
    publisher: 'Hogarth Press',
    rating: 5,
    tags: ['modernism', 'stream of consciousness', 'british literature', 'experimental fiction', 'psychological fiction'],
    categories: ['Fiction', 'Classic Literature', 'Modernism']
  },
  {
    id: 'the-stranger',
    book_id: 'the-stranger',
    title: 'The Stranger',
    slug: 'the-stranger-by-albert-camus',
    contributors: [
      { role: 'author', person: 'albert-camus' }
    ],
    published_date: '1942',
    description: 'A story of an ordinary man who unwittingly gets drawn into a senseless murder on an Algerian beach.',
    excerpt: 'A story of an ordinary man who unwittingly gets drawn into a senseless murder on an Algerian beach.',
    content: `<p>The Stranger (French: L'Étranger) is a novel by Albert Camus, published in 1942. Its theme and outlook are often cited as examples of Camus's philosophy, absurdism coupled with existentialism, though Camus personally rejected the latter label.</p>
    <p>The narrative follows Meursault, an indifferent French Algerian who, after attending his mother's funeral, kills an Arab man in French Algiers. The novel is divided into two parts: the first part chronicles the days leading up to the murder, including Meursault's mother's funeral, his forming of a relationship with Marie, and his friendship with Raymond; the second part follows Meursault's imprisonment, trial, and sentence.</p>
    <p>The novel is characterized by Meursault's emotional detachment from the events around him, including his mother's death and his own trial. His indifference to societal expectations, particularly regarding displays of grief and remorse, ultimately leads to his condemnation. Throughout the narrative, Camus explores themes of absurdity, meaninglessness, and the human search for purpose in an indifferent universe.</p>`,
    period: '20th Century',
    page_count: 159,
    isbn13: '9780679720201',
    genre: 'Modern Literature',
    publisher: 'Gallimard',
    rating: 5,
    tags: ['absurdism', 'existentialism', 'french literature', 'philosophical fiction', 'modernism'],
    categories: ['Fiction', 'Classic Literature', 'Philosophy']
  },
  {
    id: 'the-plague',
    book_id: 'the-plague',
    title: 'The Plague',
    slug: 'the-plague-by-albert-camus',
    contributors: [
      { role: 'author', person: 'albert-camus' }
    ],
    published_date: '1947',
    description: 'A novel about a town hit by a plague that brings about the isolation and existential questioning of its inhabitants.',
    excerpt: 'A novel about a town hit by a plague that brings about the isolation and existential questioning of its inhabitants.',
    content: `<p>The Plague (French: La Peste) is a novel by Albert Camus, published in 1947. It tells the story of a plague sweeping the French Algerian city of Oran. It asks a number of questions relating to the nature of destiny and the human condition. The characters in the book, ranging from doctors to vacationers to fugitives, all help to show the effects the plague has on a populace.</p>
    <p>The narrative is presented as a chronicle by an unnamed narrator, later revealed to be Dr. Bernard Rieux. The story follows various characters as they grapple with the epidemic: Dr. Rieux, who tries to combat the plague medically; Raymond Rambert, a journalist who initially attempts to escape the quarantined city to rejoin his wife in Paris; Jean Tarrou, an enigmatic visitor who organizes a team of volunteers to help fight the epidemic; Joseph Grand, a municipal clerk working on a novel; and Father Paneloux, a Jesuit priest who interprets the plague as divine punishment.</p>
    <p>The novel explores themes of solidarity in the face of suffering, the human capacity for compassion, and the absurdity of existence in a seemingly indifferent universe. Camus uses the plague as a metaphor for the human condition and the evils that afflict humanity, such as war, totalitarianism, and indifference to suffering.</p>`,
    period: '20th Century',
    page_count: 308,
    isbn13: '9780679720218',
    genre: 'Modern Literature',
    publisher: 'Gallimard',
    rating: 5,
    tags: ['absurdism', 'existentialism', 'french literature', 'philosophical fiction', 'epidemic fiction'],
    categories: ['Fiction', 'Classic Literature', 'Philosophy']
  },
  {
    id: 'simulacra-and-simulation',
    book_id: 'simulacra-and-simulation',
    title: 'Simulacra and Simulation',
    slug: 'simulacra-and-simulation',
    contributors: [
      { role: 'author', person: 'jean-baudrillard', person_name: 'Jean Baudrillard' },
      { role: 'translator', person: 'sheila-faria-glaser', person_name: 'Sheila Faria Glaser' }
    ],
    published_date: '1981',
    period: 'Postmodern',
    page_count: 164,
    genre: 'Philosophy',
    publisher: 'Éditions Galilée',
    excerpt: 'A philosophical treatise exploring how signs and symbols have replaced reality in contemporary society, creating a hyperreality of simulacra.',
    description: 'Simulacra and Simulation is a philosophical treatise by Jean Baudrillard that discusses the relationships between reality, symbols, and society. Baudrillard claims that modern society has replaced all reality and meaning with symbols and signs, and that human experience is of a simulation of reality rather than reality itself. The simulacra that Baudrillard refers to are the signs of culture and media that create the perceived reality; Baudrillard believed that society has become so saturated with these simulacra that it has lost contact with the real world on which the simulacra are based.',
    tags: ['philosophy', 'postmodernism', 'media theory', 'simulation', 'semiotics'],
    poster_image: '/images/books/simulacra-and-simulation_poster.jpg',
    cover_image: '/images/books/simulacra-and-simulation_cover.jpg',
  },
  {
    id: 'blood-meridian',
    book_id: 'blood-meridian',
    title: 'Blood Meridian',
    slug: 'blood-meridian',
    contributors: [
      { role: 'author', person: 'cormac-mccarthy', person_name: 'Cormac McCarthy' }
    ],
    published_date: '1985',
    period: 'Contemporary',
    page_count: 337,
    genre: 'Western',
    publisher: 'Random House',
    excerpt: 'An epic and violent vision of the American West following a teenage runaway who joins a gang of scalp hunters along the US-Mexico border in the 1850s.',
    description: 'Blood Meridian or The Evening Redness in the West is a 1985 epic Western novel by American author Cormac McCarthy. The book is based on historical events that took place on the Texas-Mexico border in the 1850s and traces the journey of the Kid, a 14-year-old Tennessean who stumbles into a nightmarish world when he joins a ruthless gang of scalp hunters. The novel is characterized by its graphic violence and McCarthy\'s distinctive writing style, which features archaic vocabulary, biblical cadences, and a lack of conventional punctuation. Critics have described it as one of the greatest novels in American literature, with its bleak view of frontier violence and its exploration of human depravity.',
    tags: ['western', 'historical fiction', 'violence', 'american west', 'philosophical'],
    poster_image: '/images/books/blood-meridian_poster.jpg',
    cover_image: '/images/books/blood-meridian_cover.jpg',
  },
  {
    id: 'house-of-leaves',
    book_id: 'house-of-leaves',
    title: 'House of Leaves',
    slug: 'house-of-leaves',
    contributors: [
      { role: 'author', person: 'mark-z-danielewski', person_name: 'Mark Z. Danielewski' }
    ],
    published_date: '2000',
    period: 'Contemporary',
    page_count: 709,
    genre: 'Experimental Fiction',
    publisher: 'Pantheon Books',
    excerpt: 'An experimental novel about a young family that discovers their house is bigger on the inside than the outside, presented through multiple narrators and unconventional typography.',
    description: 'House of Leaves is the debut novel by American author Mark Z. Danielewski, published in March 2000 by Pantheon Books. A bestseller, it has been translated into a number of languages. The novel has a unique and unconventional format, containing multiple narrators, extensive footnotes, colored text, and unusual page layouts. Some pages contain only a few words or lines of text, arranged in strange shapes, while others are densely packed with text in various formats. The novel tells the story of a young family that moves into a small home on Ash Tree Lane where they discover their house is bigger on the inside than the outside. The format and structure of the novel is unconventional, with multiple narrators, typographical variations, and a labyrinthine structure that mirrors the house in the story.',
    tags: ['experimental', 'horror', 'postmodern', 'metafiction', 'unconventional typography'],
    poster_image: '/images/books/house-of-leaves_poster.jpg',
    cover_image: '/images/books/house-of-leaves_cover.jpg',
  },
  {
    id: 'if-on-a-winters-night-a-traveler',
    book_id: 'if-on-a-winters-night-a-traveler',
    title: 'If on a winter\'s night a traveler',
    slug: 'if-on-a-winters-night-a-traveler',
    contributors: [
      { role: 'author', person: 'italo-calvino', person_name: 'Italo Calvino' },
      { role: 'translator', person: 'william-weaver', person_name: 'William Weaver' }
    ],
    published_date: '1979',
    period: 'Postmodern',
    page_count: 260,
    genre: 'Postmodern Literature',
    publisher: 'Einaudi',
    excerpt: 'A novel about a reader trying to read a novel called "If on a winter\'s night a traveler," structured as a series of interrupted beginnings of different novels.',
    description: 'If on a winter\'s night a traveler (Italian: Se una notte d\'inverno un viaggiatore) is a 1979 postmodernist novel by Italian writer Italo Calvino. The narrative, in the form of a frame story, is about the reader trying to read a book called If on a winter\'s night a traveler. Each odd-numbered chapter is in the second person, and tells the reader what they are doing in preparation for reading the next chapter. The even-numbered chapters are the first chapter of new books that the reader finds. The reader is highly self-aware and constantly addresses "you," the actual reader of the physical book.',
    tags: ['postmodern', 'metafiction', 'italian literature', 'frame story', 'books about reading'],
    poster_image: '/images/books/if-on-a-winters-night-a-traveler_poster.jpg',
    cover_image: '/images/books/if-on-a-winters-night-a-traveler_cover.jpg',
  },
  {
    id: 'pedro-paramo',
    book_id: 'pedro-paramo',
    title: 'Pedro Páramo',
    slug: 'pedro-paramo',
    contributors: [
      { role: 'author', person: 'juan-rulfo', person_name: 'Juan Rulfo' },
      { role: 'translator', person: 'margaret-sayers-peden', person_name: 'Margaret Sayers Peden' }
    ],
    published_date: '1955',
    period: 'Modernist',
    page_count: 124,
    genre: 'Magical Realism',
    publisher: 'Fondo de Cultura Económica',
    excerpt: 'A man travels to his recently deceased mother\'s hometown to find his father, only to discover a ghost town populated by spirits and echoes of the past.',
    description: 'Pedro Páramo is a novel written by Juan Rulfo about a man named Juan Preciado who travels to his recently deceased mother\'s hometown, Comala, to find his father, Pedro Páramo. The novel is set in the aftermath of the Mexican Revolution and combines elements of magical realism, surrealism, and the gothic. The town of Comala is populated with the ghosts of its former inhabitants, and the narrative structure is non-linear, with shifts between past and present, reality and dream, and the perspectives of the living and the dead. Pedro Páramo is considered one of the most important novels in 20th-century Latin American literature and a precursor to the magical realism movement. It has influenced many authors, including Gabriel García Márquez.',
    tags: ['magical realism', 'mexican literature', 'ghosts', 'non-linear narrative', 'surrealism'],
    poster_image: '/images/books/pedro-paramo_poster.jpg',
    cover_image: '/images/books/pedro-paramo_cover.jpg',
  },
  {
    id: 'invisible-cities',
    book_id: 'invisible-cities',
    title: 'Invisible Cities',
    slug: 'invisible-cities',
    contributors: [
      { role: 'author', person: 'italo-calvino', person_name: 'Italo Calvino' },
      { role: 'translator', person: 'william-weaver', person_name: 'William Weaver' }
    ],
    published_date: '1972',
    period: 'Postmodern',
    page_count: 165,
    genre: 'Fiction',
    publisher: 'Einaudi',
    excerpt: 'A series of prose poems describing fictitious cities, framed as a conversation between Marco Polo and Kublai Khan.',
    description: 'Invisible Cities (Italian: Le città invisibili) is a novel by Italian writer Italo Calvino. It was published in Italy in 1972. The book explores imagination and the imaginable through descriptions of cities by an explorer, Marco Polo. The book is framed as a conversation between the elderly and busy emperor Kublai Khan, who constantly has merchants coming to describe the state of his expanding empire, and Polo, who cannot speak Kublai\'s language. They communicate through gestures, objects, and finally through their own languages, as Polo gradually learns the Khan\'s language. The majority of the book consists of brief prose poems describing 55 fictitious cities that are all narrated by Polo, many of which can be read as parables or meditations on culture, language, time, memory, death, or the general nature of human experience.',
    tags: ['postmodern', 'italian literature', 'prose poetry', 'cities', 'marco polo'],
    poster_image: '/images/books/invisible-cities_poster.jpg',
    cover_image: '/images/books/invisible-cities_cover.jpg',
  },
  {
    id: 'ficciones',
    book_id: 'ficciones',
    title: 'Ficciones',
    slug: 'ficciones',
    contributors: [
      { role: 'author', person: 'jorge-luis-borges', person_name: 'Jorge Luis Borges' },
      { role: 'translator', person: 'anthony-kerrigan', person_name: 'Anthony Kerrigan' }
    ],
    published_date: '1944',
    period: 'Modernist',
    page_count: 174,
    genre: 'Short Stories',
    publisher: 'Editorial Sur',
    excerpt: 'A collection of short stories that blend elements of fantasy, philosophy, and literary criticism, exploring themes of infinity, labyrinths, and the nature of reality.',
    description: 'Ficciones is a collection of short stories by Argentine writer and poet Jorge Luis Borges, originally published in 1944. The collection\'s English translation was among the first to win the National Book Award for Translation.The stories in Ficciones are characterized by their philosophical and metaphysical themes, as well as their use of fantasy and surrealism.Many of them deal with themes such as infinity, recursion, reality, consciousness, and identity.Borges\' innovative style combines elements of fiction with non-fiction genres such as essays and literary criticism. The stories often involve elaborate imaginary worlds, metafictional elements, and intellectual puzzles, influencing generations of writers in the magical realist and postmodern traditions.',
    tags: ['short stories', 'argentinian literature', 'magical realism', 'philosophy', 'metafiction'],
    poster_image: '/images/books/ficciones_poster.jpg',
    cover_image: '/images/books/ficciones_cover.jpg',
  },
  {
    id: 'the-unconsoled',
    book_id: 'the-unconsoled',
    title: 'The Unconsoled',
    slug: 'the-unconsoled',
    contributors: [
      { role: 'author', person: 'kazuo-ishiguro', person_name: 'Kazuo Ishiguro' }
    ],
    published_date: '1995',
    period: 'Contemporary',
    page_count: 535,
    genre: 'Surrealist Fiction',
    publisher: 'Faber and Faber',
    excerpt: 'A renowned pianist arrives in a Central European city to give a concert, only to find himself entangled in a dreamlike series of events and obligations.',
    description: 'The Unconsoled is a novel by Kazuo Ishiguro, first published in 1995. The novel is about Ryder, a famous pianist who arrives in a Central European city to perform a concert. However, from the beginning, the novel subverts expectations with its dreamlike, often surreal narrative. Time and space are fluid, with locations suddenly transforming and distances expanding or contracting unexpectedly. Ryder often finds himself in situations without knowing how he got there, and he seems to know people he has never met before. The novel has been described as "a novel of dream logic," with its strange, shifting reality and its protagonist\'s continual frustration as he tries to fulfill his obligations. The Unconsoled explores themes of memory, identity, and the sense of duty that can sometimes overshadow personal relationships.',
    tags: ['surrealism', 'dream logic', 'music', 'memory', 'identity'],
    poster_image: '/images/books/the-unconsoled_poster.jpg',
    cover_image: '/images/books/the-unconsoled_cover.jpg',
  },
  {
    id: 'the-master-and-margarita',
    book_id: 'the-master-and-margarita',
    title: 'The Master and Margarita',
    slug: 'the-master-and-margarita',
    contributors: [
      { role: 'author', person: 'mikhail-bulgakov', person_name: 'Mikhail Bulgakov' },
      { role: 'translator', person: 'richard-pevear', person_name: 'Richard Pevear' },
      { role: 'translator', person: 'larissa-volokhonsky', person_name: 'Larissa Volokhonsky' }
    ],
    published_date: '1967',
    period: 'Modernist',
    page_count: 384,
    genre: 'Satire',
    publisher: 'YMCA Press',
    excerpt: 'A satirical novel that blends supernatural elements with a scathing critique of Soviet life, centered around the Devil\'s visit to atheistic Moscow.',
    description: 'The Master and Margarita (Russian: Мастер и Маргарита) is a novel by Russian writer Mikhail Bulgakov, written in the Soviet Union between 1928 and 1940 during Stalin\'s regime. A censored version was published in Moscow magazine in 1966–1967, after the writer\'s death. The novel combines supernatural elements with satirical dark comedy and Christian philosophy, defying categorization within a single genre. The story concerns a visit by the devil to the officially atheistic Soviet Union. The novel alternates between two settings: contemporary Moscow and Jerusalem during the time of Pontius Pilate. While many critics consider it to be one of the best novels of the 20th century, it has also been recognized for its political criticism of Soviet society, particularly its literary establishment and atheistic social policies.',
    tags: ['russian literature', 'satire', 'supernatural', 'soviet union', 'religion'],
    poster_image: '/images/books/the-master-and-margarita_poster.jpg',
    cover_image: '/images/books/the-master-and-margarita_cover.jpg',
  },
  {
    id: 'pale-fire',
    book_id: 'pale-fire',
    title: 'Pale Fire',
    slug: 'pale-fire',
    contributors: [
      { role: 'author', person: 'vladimir-nabokov', person_name: 'Vladimir Nabokov' }
    ],
    published_date: '1962',
    period: 'Postmodern',
    page_count: 315,
    genre: 'Fiction',
    publisher: 'G. P. Putnam\'s Sons',
    excerpt: 'A novel consisting of a 999-line poem by a fictional poet and an extensive commentary by a possibly delusional academic.',
    description: 'Pale Fire is a 1962 novel by Vladimir Nabokov. The novel is presented as a 999-line poem titled "Pale Fire," written by the fictional poet John Shade, with a foreword, extensive commentary, and index written by Shade\'s neighbor and academic colleague, Charles Kinbote. Together these elements form a narrative in which both fictional authors are central characters. The novel begins with Kinbote\'s foreword, which contains the information that Shade was killed by an assassin shortly after completing his poem. The novel consists of Kinbote\'s elaborate commentary on the poem, which is filled with surprisingly little discussion of the poem itself. Instead, Kinbote uses the commentary to tell his own story, which involves the exiled king of a country called Zembla, who fled a revolutionary regime and is being hunted by an assassin. As the narrative progresses, the reader begins to question Kinbote\'s sanity and the reliability of his account.',
    tags: ['metafiction', 'unreliable narrator', 'russian-american literature', 'poetry', 'academia'],
    poster_image: '/images/books/pale-fire_poster.jpg',
    cover_image: '/images/books/pale-fire_cover.jpg',
  },
];

/**
 * Utility functions to work with books data
 */

// Get a book by its ID
export const getBookById = (id: string): Book | undefined => {
  return books.find(book => book.id === id || book.book_id === id);
};

// Get a book by its slug
export const getBookBySlug = (slug: string): Book | undefined => {
  return books.find(book => book.slug === slug);
};

// Get all books
export const getAllBooks = (): Book[] => {
  return books;
};

// Get books by author (person ID)
export const getBooksByAuthor = (authorId: string): Book[] => {
  return books.filter(book =>
    book.contributors.some(contributor =>
      contributor.role === 'author' && contributor.person === authorId
    )
  );
};

// Get books by genre
export const getBooksByGenre = (genre: string): Book[] => {
  return books.filter(book => book.genre === genre);
};

// Get books by tag
export const getBooksByTag = (tag: string): Book[] => {
  return books.filter(book => book.tags?.includes(tag));
};

// Get books by category
export const getBooksByCategory = (category: string): Book[] => {
  return books.filter(book => book.categories?.includes(category));
};

// Get books by period
export const getBooksByPeriod = (period: string): Book[] => {
  return books.filter(book => book.period === period);
};

// Search books by title
export const searchBooksByTitle = (query: string): Book[] => {
  const lowercaseQuery = query.toLowerCase();
  return books.filter(book =>
    book.title.toLowerCase().includes(lowercaseQuery)
  );
};

// Get latest books
export const getLatestBooks = (count: number = 3): Book[] => {
  return [...books].slice(0, count);
};
