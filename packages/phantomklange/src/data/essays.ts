// packages/phantomklange/src/data/essays.ts
// @ts-nocheck

/**
 * Mock database of essays
 */
import { Essay } from './types';

// Sample essays data - in production, this would come from a database
// TODO: Remove this once we have a real data source
export const essays: Essay[] = [
  {
    id: 'dark-aesthetics',
    essay_id: 'dark-aesthetics',
    title: 'The Dark Aesthetics of Digital Space',
    slug: 'dark-aesthetics-digital-space',
    author_id: 'yourusername',
    author_name: 'Your Name',
    publication_date: '2023-11-17',
    last_updated: '2024-06-10',
    reading_time: 12,
    collaborators: [
      {
        role: 'editor',
        person: 'roland-barthes',
        person_slug: 'roland-barthes',
        person_name: 'Roland Barthes'
      }
    ],
    excerpt: 'An exploration of the philosophical implications of dark mode interfaces and how they reflect our changing relationship with digital spaces.',
    tags: ['design', 'philosophy', 'digital', 'aesthetics'],
    categories: ['essays', 'design-theory'],
    markdown_content: `
# The Dark Aesthetics of Digital Space

In the evolving landscape of digital interfaces, the rise of "dark mode" represents more than just an aesthetic preference—it embodies a philosophical shift in how we perceive and inhabit digital spaces. This essay explores the phenomenological implications of darkness as a default state in our most intimate technological environments.

## The Inversion of Light and Darkness

For centuries, Western thought has equated light with knowledge and darkness with ignorance. The Enlightenment itself took illumination as its central metaphor. Yet in our digital halls, we increasingly choose darkness as our preferred mode of operation. What does this inversion signify?

> "Perhaps this preference for darkness represents not a turn toward ignorance, but an acknowledgment that the relentless luminosity of screens requires moderation—a digital chiaroscuro that preserves both our attention and our vision."

The bright white page, once the unquestioned default of digital interfaces, mimicked its physical predecessor. But as screens became our primary reading surfaces, their fundamental difference from paper became impossible to ignore: screens *emit* light rather than merely reflecting it.

### The Physiology of Digital Reading

Research has shown that prolonged exposure to bright screens, particularly in low-light environments, can lead to:

- Increased eye strain
- Disrupted melatonin production
- Potential long-term vision issues
- Cognitive fatigue

But the shift toward dark interfaces isn't merely physiological—it represents a maturing relationship with digital technology, an acknowledgment of its unique properties rather than an imitation of physical media.

## The Phenomenology of Digital Darkness

When we enter a dark-mode interface, we experience a curious inversion: the device recedes, and the content emerges. Text and images float in an undefined space, untethered from physical constraints. This creates what philosopher Maurice Merleau-Ponty might call a different "field of presence"—the dark interface alters our perceptual engagement with digital content.

### Code Sample: Dark Mode Implementation

\`\`\`css
:root {
  --light-bg: #ffffff;
  --light-text: #1a1a1a;
  --dark-bg: #121212;
  --dark-text: #e0e0e0;
}

@media (prefers-color-scheme: dark) {
  body {
    background-color: var(--dark-bg);
    color: var(--dark-text);
  }
}

.dark-mode {
  background-color: var(--dark-bg);
  color: var(--dark-text);
}
\`\`\`

## Digital Chiaroscuro: The Play of Light and Shadow

Renaissance painters mastered chiaroscuro—the use of strong contrasts between light and dark—to create depth and drama. In digital spaces, we create our own form of chiaroscuro through carefully calibrated interfaces where text and image emerge from darkness, creating a depth that draws us in.

| Interface Type | Background | Text | Contrast Ratio | WCAG Compliance |
|---------------|------------|------|----------------|-----------------|
| Light Mode    | #FFFFFF    | #333333 | 12.63:1      | AAA (Pass)      |
| Dark Mode     | #121212    | #E0E0E0 | 14.97:1      | AAA (Pass)      |
| Sepia Mode    | #F5EFE0    | #5F4B32 | 9.87:1       | AAA (Pass)      |

## The Ethics of Interface Darkness

There are deeper implications to our preference for digital darkness. Dark interfaces:

1. **Consume less power** on OLED and AMOLED screens
2. **Create less light pollution** in shared spaces
3. **Signal sophistication** and technical knowledge
4. **Create a sense of intimacy** in public settings

As our physical and digital worlds increasingly blend, the aesthetic choices we make in digital spaces carry over into physical design. The minimalist dark aesthetics of digital interfaces now influence architecture, fashion, and product design.

![Dark mode interface example](/images/essays/dark-aesthetics-digital-space/dark-interface.jpg)

## Conclusion: Embracing the Digital Night

Our embrace of dark interfaces suggests a maturing relationship with digital technology—one that no longer seeks to merely imitate physical media, but rather acknowledges the unique properties of digital space. As we spend increasing portions of our lives in these spaces, choosing darkness as our default mode might represent a desire for digital environments that soothe rather than stimulate, that recede rather than demand attention.

In the endless day of digital connectivity, perhaps dark mode offers us a much-needed night.

***

## References

* Johnson, A. (2022). *The Psychology of User Interface Design*. Digital Press.
* Smith, J. & Wesson, L. (2021). "Impact of Interface Brightness on Cognitive Load." *Journal of Human-Computer Interaction*, 35(4), 112-128.
* Merleau-Ponty, M. (1945). *Phenomenology of Perception*. Gallimard.
`,
    related_works: [
      {
        id: 'the-work-of-art-in-the-age-of-mechanical-reproduction',
        title: 'The Work of Art in the Age of Mechanical Reproduction',
        type: 'essay',
        slug: 'the-work-of-art-in-the-age-of-mechanical-reproduction'
      },
      {
        id: 'being-and-time',
        title: 'Being and Time',
        type: 'book',
        slug: 'being-and-time'
      }
    ]
  },
  {
    id: 'death-of-the-author',
    essay_id: 'death-of-the-author',
    title: 'The Death of the Author: Revisited',
    slug: 'death-of-the-author-revisited',
    author_id: 'yourusername',
    author_name: 'Your Name',
    publication_date: '2023-08-22',
    last_updated: '2023-09-15',
    reading_time: 8,
    collaborators: [
      {
        role: 'researcher',
        person: 'roland-barthes',
        person_slug: 'roland-barthes',
        person_name: 'Roland Barthes'
      }
    ],
    excerpt: 'A modern reexamination of Roland Barthes\' famous essay in the age of AI-generated content and digital authorship.',
    tags: ['literary criticism', 'philosophy', 'AI', 'authorship'],
    categories: ['essays', 'literary-theory'],
    markdown_content: `
# The Death of the Author: Revisited

In 1967, Roland Barthes published his landmark essay "The Death of the Author," arguing against incorporating the intentions and biographical context of an author in the interpretation of a text. More than half a century later, we find ourselves in a world where the concept of authorship faces new challenges from AI-generated content and collaborative digital platforms.

## Barthes' Original Argument

Barthes posited that to assign a text a single, corresponding author is to impose a limit on that text. By focusing on the author, critics were neglecting the reader's role in bringing meaning to a text. In Barthes' view, a text's meaning lay not in its origin but in its destination—the reader.

> "The birth of the reader must be at the cost of the death of the Author."
> — Roland Barthes, 1967

This view represented a significant shift from traditional literary criticism, which often sought to discover the author's intentions as a way to unlock a text's "true" meaning.

## The Digital Transformation of Authorship

Today, authorship has been transformed by digital technologies in ways Barthes could not have anticipated:

1. **Collaborative Creation**: Wikis, open-source projects, and collaborative fiction platforms blur the lines of individual authorship
2. **Remixing and Sampling**: Digital media allows for the recombination of existing works into new creations
3. **AI-Generated Content**: Language models can now produce coherent, creative text without human authorship
4. **Reader Interaction**: Interactive fiction and games allow readers to co-create narratives

As we navigate these new forms of textual production, Barthes' theories gain renewed relevance. When an AI system generates a poem, who is the author? The programmers? The training data creators? The AI itself? The person who prompted the system?
`,
    related_works: [
      {
        id: 'the-death-of-the-author',
        title: 'The Death of the Author',
        type: 'essay',
        slug: 'the-death-of-the-author-by-roland-barthes'
      }
    ]
  },
  {
    id: 'the-death-of-the-author',
    title: 'The Death of the Author',
    slug: 'the-death-of-the-author-by-roland-barthes',
    contributors: [
      { role: 'author', person: 'roland-barthes' }
    ],
    publication_date: '1967',
    description: 'A landmark essay arguing against traditional literary criticism\'s practice of incorporating the intentions and biographical context of an author in an interpretation of a text.',
    excerpt: 'A landmark essay arguing against traditional literary criticism\'s practice of incorporating the intentions and biographical context of an author in an interpretation of a text.',
    content: `<p>The Death of the Author is a 1967 essay by the French literary critic and theorist Roland Barthes. Barthes's essay argues against traditional literary criticism's practice of incorporating the intentions and biographical context of an author in an interpretation of a text. Instead, the essay emphasizes that the meaning of a text should be interpreted solely by readers, separate from the intentions and context of the author.</p>
    <p>Barthes's argument against the method of reading that relies on aspects of the author's identity to distill meaning from the author's work is that the method of reading places unnecessary limits on a text. Instead, Barthes asks the reader to consider the text based on its own merits, without the biographical context or intent of the author. "The death of the author" as a critical position, then, is the rejection of the idea that a text's author has the definitive say on how that text should be interpreted.</p>
    <p>The essay's first English-language publication was in the American journal Aspen, no. 5–6 in 1967; the French text was published in 1968. "The Death of the Author" became one of his most famous and referenced works.</p>`,
    tags: ['literary theory', 'structuralism', 'post-structuralism', 'critical theory', 'literary criticism'],
    categories: ['Literary Theory', 'Philosophy']
  },
  {
    id: 'the-myth-of-sisyphus',
    title: 'The Myth of Sisyphus',
    slug: 'the-myth-of-sisyphus-by-albert-camus',
    contributors: [
      { role: 'author', person: 'albert-camus' }
    ],
    publication_date: '1942',
    description: 'A philosophical essay that introduces Camus\'s philosophy of the absurd: the futile search for meaning in an unintelligible world devoid of God and eternal truths.',
    excerpt: 'A philosophical essay that introduces Camus\'s philosophy of the absurd: the futile search for meaning in an unintelligible world devoid of God and eternal truths.',
    content: `<p>The Myth of Sisyphus is a philosophical essay by Albert Camus that introduces his philosophy of the absurd. The essay begins with the premise that life is absurd and ultimately meaningless, a conflict between human beings' desire for meaning and purpose and the silent, unintelligible world they inhabit.</p>
    <p>The essay's title refers to the Greek mythological figure Sisyphus, who was condemned to repeatedly roll a boulder up a hill only to have it roll back down again for eternity. Camus uses this story as a metaphor for the human condition. In his interpretation, Sisyphus represents the absurdity of human life, endlessly performing meaningless tasks.</p>
    <p>However, Camus concludes, "One must imagine Sisyphus happy." He suggests that the recognition and acceptance of absurdity can become an act of revolt, allowing one to find meaning in the process of struggling with it. Camus argues that by acknowledging the absurdity of seeking meaning in a meaningless world, one can actually find happiness in the struggle itself.</p>`,
    tags: ['existentialism', 'absurdism', 'philosophy', 'meaning of life', 'greek mythology'],
    categories: ['Philosophy', 'Existentialism'],
    related_works: ['/books/the-stranger-by-albert-camus']
  },
  {
    id: 'a-room-of-ones-own',
    title: 'A Room of One\'s Own',
    slug: 'a-room-of-ones-own-by-virginia-woolf',
    contributors: [
      { role: 'author', person: 'virginia-woolf' }
    ],
    publication_date: '1929',
    description: 'An extended essay arguing for both a literal and figurative space for women writers within a literary tradition dominated by men.',
    excerpt: 'An extended essay arguing for both a literal and figurative space for women writers within a literary tradition dominated by men.',
    content: `<p>A Room of One's Own is an extended essay by Virginia Woolf, first published in September 1929. The work is based on two lectures Woolf delivered at Newnham College and Girton College, women's colleges at the University of Cambridge in October 1928. While this extended essay employs a fictional narrator and narrative to explore women both as writers and characters in fiction, the manuscript for the delivery of the series of lectures, titled "Women and Fiction", and hence the essay, is considered non-fiction.</p>
    <p>The essay examines whether women were capable of producing, and in fact free to produce, work of the quality of William Shakespeare, addressing the limitations that past and present women writers faced. Woolf argues that, "a woman must have money and a room of her own if she is to write fiction." This simple statement has become an iconic feminist text, arguing that women have been denied the freedom (both financial and personal) to create art.</p>
    <p>Woolf's essay explores the history of women's writing and the financial, educational, and social difficulties women faced in producing literature. She examines how male dominance has shaped literary history and culture, and argues for the importance of having a physical space and financial independence for women to develop their creativity.</p>`,
    tags: ['feminism', 'literary criticism', 'women writers', 'gender inequality', 'social critique'],
    categories: ['Literary Criticism', 'Feminism', 'Gender Studies'],
    related_works: ['/books/to-the-lighthouse-by-virginia-woolf']
  },
  {
    id: 'the-work-of-art',
    title: 'The Work of Art in the Age of Mechanical Reproduction',
    slug: 'the-work-of-art-in-the-age-of-mechanical-reproduction-by-walter-benjamin',
    contributors: [
      { role: 'author', person: 'walter-benjamin' }
    ],
    publication_date: '1935',
    description: 'A seminal essay exploring how modern technologies of reproduction have changed the nature of art and its reception.',
    excerpt: 'A seminal essay exploring how modern technologies of reproduction have changed the nature of art and its reception.',
    content: `<p>The Work of Art in the Age of Mechanical Reproduction (German: Das Kunstwerk im Zeitalter seiner technischen Reproduzierbarkeit) is a 1935 essay by German cultural critic Walter Benjamin that explores the changing nature of art in modern society, particularly in light of new technologies that allow for mass reproduction of artworks.</p>
    <p>Benjamin introduces the concept of an artwork's "aura," which he describes as the sense of reverence and uniqueness that traditional artworks possess due to their authenticity, historical testimony, and cultural authority. He argues that mechanical reproduction—through technologies like photography and film—undermines this aura by removing art from its traditional context and enabling identical copies to be distributed widely.</p>
    <p>However, Benjamin does not simply lament this loss. Instead, he sees the decline of the aura as potentially liberating, as it democratizes access to art and undermines the elitism of traditional aesthetic values. He particularly celebrates film as a revolutionary art form that can create new forms of perception and experience. At the same time, he warns about the dangers of aestheticizing politics, particularly in fascism, which he contrasts with communism's politicization of art.</p>`,
    tags: ['art theory', 'critical theory', 'technology', 'modernism', 'cultural criticism'],
    categories: ['Critical Theory', 'Art Theory']
  },
  {
    id: 'the-second-sex',
    title: 'The Second Sex',
    slug: 'the-second-sex-by-simone-de-beauvoir',
    contributors: [
      { role: 'author', person: 'simone-de-beauvoir' }
    ],
    publication_date: '1949',
    description: 'A groundbreaking analysis of women\'s oppression and a foundational text for modern feminism.',
    excerpt: 'A groundbreaking analysis of women\'s oppression and a foundational text for modern feminism.',
    content: `<p>The Second Sex (French: Le Deuxième Sexe) is a 1949 book by the French existentialist philosopher Simone de Beauvoir, in which she discusses the treatment of women throughout history. It is often regarded as a major work of feminist philosophy and the starting point of second-wave feminism.</p>
    <p>De Beauvoir's central thesis is that women have been held in a relationship of long-standing oppression to men through being cast as the "Other." She uses the existentialist ethics developed by herself and Jean-Paul Sartre to criticize the situation of women in male-dominated society. Her analysis focuses on the social construction of Woman as the quintessential Other. She argues that women are as capable of choice as men, and thus can choose to elevate themselves, moving beyond the "immanence" to which they were previously resigned and reaching "transcendence," a position in which one takes responsibility for oneself and the world.</p>
    <p>The book contains de Beauvoir's famous line, "One is not born, but rather becomes, a woman," which introduces her concept that femininity is a social construct imposed on female bodies by external forces, rather than an inherent quality of women. This distinction between sex and gender has been hugely influential in feminist theory.</p>`,
    tags: ['feminism', 'existentialism', 'gender studies', 'women\'s rights', 'philosophy'],
    categories: ['Feminism', 'Philosophy', 'Gender Studies']
  }
];

/**
 * Utility functions to work with essays data
 */

// Get an essay by its ID
export const getEssayById = (id: string): Essay | undefined => {
  return essays.find(essay => essay.id === id);
};

// Get an essay by its slug
export const getEssayBySlug = (slug: string): Essay | undefined => {
  return essays.find(essay => essay.slug === slug);
};

// Get all essays
export const getAllEssays = (): Essay[] => {
  return essays;
};

// Get essays by author (person ID)
export const getEssaysByAuthor = (authorId: string): Essay[] => {
  return essays.filter(essay =>
    essay.contributors.some(contributor =>
      contributor.role === 'author' && contributor.person === authorId
    )
  );
};

// Get essays by tag
export const getEssaysByTag = (tag: string): Essay[] => {
  return essays.filter(essay => essay.tags?.includes(tag));
};

// Get essays by category
export const getEssaysByCategory = (category: string): Essay[] => {
  return essays.filter(essay => essay.categories?.includes(category));
};

// Search essays by title
export const searchEssaysByTitle = (query: string): Essay[] => {
  const lowercaseQuery = query.toLowerCase();
  return essays.filter(essay =>
    essay.title.toLowerCase().includes(lowercaseQuery)
  );
};

export const getLatestEssays = (count: number = 3): Essay[] => {
  // Sort by publication date (newest first) and take the requested number
  return [...essays]
    .sort((a, b) => new Date(b.publication_date).getTime() - new Date(a.publication_date).getTime())
    .slice(0, count);
};

export const getRelatedEssays = (essayId: string, count: number = 2): Essay[] => {
  const currentEssay = getEssayById(essayId);
  if (!currentEssay) return [];

  // Get essays that share tags with the current essay
  const relatedByTags = essays.filter(essay =>
    essay.id !== essayId &&
    essay.tags?.some(tag => currentEssay.tags?.includes(tag))
  );

  return relatedByTags.slice(0, count);
};
