export class Advertisement {
    id: number;
    title: string;
    owner: string;
    description: string;
    category: string | null;
    views: number;
    date_start: Date;
    date_end: Date;
    content?: string;

    constructor(id: number, title: string, owner: string, description: string, category: string | null, views: number, date_start: Date | string, date_end: Date | string) {
        this.id = id;
        this.title = title;
        this.owner = owner;
        this.description = description;
        this.category = category;
        this.views = views;
        if (date_start instanceof Date) {
            this.date_start = date_start;
        }
        else {
            this.date_start = new Date(date_start);
        }

        if (date_end instanceof Date) {
            this.date_end = date_end;
        }
        else {
            this.date_end = new Date(date_end);
        }
    }
}

export class AdvertisementFillableData {
    title: string;
    description: string;
    category: string | null;
    date_start: Date;
    date_end: Date;
    content?: string;

    constructor(title: string, description: string, category: string | null, date_start: Date | string, date_end: Date | string, content: string) {
        this.title = title;
        this.description = description;
        this.category = category;
        this.content = content;

        if (date_start instanceof Date) {
            this.date_start = date_start;
        }
        else {
            this.date_start = new Date(date_start);
        }

        if (date_end instanceof Date) {
            this.date_end = date_end;
        }
        else {
            this.date_end = new Date(date_end);
        }
    }
}

export interface AdvertisementSearch {
    ordering: string | null,
    limit: number | null,
    skip: number | null,
    title__contains: string | null,
    date_start__lt: Date | null,
    date_start__gt: Date | null,
    date_end__lt: Date | null;
    date_end__gt: Date | null;
}