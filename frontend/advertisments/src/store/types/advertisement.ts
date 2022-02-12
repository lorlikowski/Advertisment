export class Advertisement {
    id: number;
    title: string;
    owner: string;
    description: string;
    views: number;
    date_start: Date;
    date_end: Date;
    content?: string;

    constructor(id: number, title: string, owner: string, description: string, views: number, date_start: Date | string, date_end: Date | string) {
        this.id = id;
        this.title = title;
        this.owner = owner;
        this.description = description;
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
    date_start: Date;
    date_end: Date;
    content?: string;

    constructor(title: string, description: string, date_start: Date, date_end: Date, content: string) {
        this.title = title;
        this.description = description;
        this.date_start = date_start;
        this.date_end = date_end;
        this.content = content;
    }
}