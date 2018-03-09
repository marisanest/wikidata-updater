import pywikibot


class WikidataItem(object):

    SITE = pywikibot.Site('wikidata', 'wikidata')
    DATA_SITE = pywikibot.site.DataSite('wikidata', 'wikidata')
    ENTITY_BASE_URI = 'https://www.wikidata.org/wiki/'

    def __init__(self, id):
        self.item = pywikibot.ItemPage.from_entity_uri(self.DATA_SITE, self.ENTITY_BASE_URI + id)

    def update(self, data):
        self.add_description(data['descriptions'])
        self.add_claims(data['claims'], data['references'])

    def add_description(self, description):
        """
        Function to add descriptions to the item.

        @param description: description
        @type description: string
        """

        self.item.editDescriptions(
            descriptions=description,
            bot=True,
            summary='New descriptions added by JudgeBot'
        )

    def add_claims(self, claims, references):

        for claim in claims:
            self.add_claim(claim)

            if 'qualifiers' in claim:
                self.add_qualifiers(claim, claim['qualifiers'])
                self.add_references(claim, references)

    def add_claim(self, claim):
        """
        Function to add a claim to the item.

        @param claim: claim
        @type claim: dict

        @return: wd_claim
        @rtype: pywikibot.page.Claim
        """

        wd_claim = pywikibot.Claim(self.DATA_SITE, claim['id'])
        wd_claim.setTarget(self.get_target(wd_claim, claim['value']))

        self.item.addClaim(
            wd_claim,
            bot=True,
            summary='New claim added by JudgeBot'
        )

        return wd_claim

    def add_qualifiers(self, claim, qualifiers):
        """
        Function to add qualifiers to a claim.

        @param claim: claim
        @type claim: pywikibot.page.Claim
        @param qualifiers: qualifiers
        @type qualifiers: dict
        """

        for qualifier in qualifiers:
            self.add_qualifier(claim, qualifier)

    def add_qualifier(self, claim, qualifier):

        wd_qualifier = pywikibot.Claim(self.DATA_SITE, qualifier['id'], isQualifier=True)
        wd_qualifier.setTarget(self.get_target(wd_qualifier, qualifier['value']))

        claim.addQualifier(
            wd_qualifier,
            bot=True,
            summary='New qualifier added by JudgeBot'
        )

    def add_references(self, claim, references):
        """
        Function to add sources to a claim.

        @param claim: claim
        @type claim: pywikibot.page.Claim
        @param references: references
        @type references: dict
        """

        wd_references = []

        for reference in references:

            wd_reference = pywikibot.Claim(self.DATA_SITE, reference['id'], isReference=True)
            wd_reference.setTarget(self.get_target(wd_reference, reference['value']))
            wd_references.append(wd_reference)

        claim.addSources(
            wd_references,
            bot=True,
            summary='New references added by JudgeBot'
        )

    def get_target(self, wd_claim, claim):

        if wd_claim.type == 'wikibase-item':
            return pywikibot.ItemPage(self.DATA_SITE, claim)
        elif wd_claim.type == 'time':
            year, month, day = claim
            return pywikibot.WbTime(year=year, month=month, day=day)
        elif wd_claim.type == 'url':
            return claim
        else:
            raise TypeError('claim type ' + wd_claim.type + ' not implemented yet')
