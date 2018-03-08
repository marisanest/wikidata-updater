from query import FindIdQuery


class Helper:
    """
    Helper class.
    """

    INSTANCE_OF_FOR_PROPERTY = {
        'P734': 'Q101352',
        'P735': 'Q202444',
        'P1559':  'Q82799',
        'P19': 'Q515'
    }

    @staticmethod
    def id_for(property, label):
        """
        Helper function to search the id for an item with the label given label.
        The item sould fit as an value for the given property.

        @param property: property
        @type property: string
        @param label: label
        @type label: string

        @return: The matching id
        @rtype: string
        """
        if property not in Helper.INSTANCE_OF_FOR_PROPERTY:
            raise ValueError(
                'property must be one of: ' + ', '.join(Helper.INSTANCE_OF_FOR_PROPERTY.keys()) + ' got ' + property)

        return FindIdQuery(Helper.INSTANCE_OF_FOR_PROPERTY[property], label).execute().extract()
