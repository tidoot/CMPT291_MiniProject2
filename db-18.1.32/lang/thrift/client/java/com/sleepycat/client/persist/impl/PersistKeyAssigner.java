/*-
 * Copyright (c) 2002, 2019 Oracle and/or its affiliates.  All rights reserved.
 *
 * See the file LICENSE for license information.
 *
 */

package com.sleepycat.client.persist.impl;

import com.sleepycat.client.bind.tuple.TupleBase;
import com.sleepycat.client.compat.DbCompat;
import com.sleepycat.client.SDatabaseEntry;
import com.sleepycat.client.SDatabaseException;
import com.sleepycat.client.SSequence;

/**
 * Assigns primary keys from a SSequence.
 *
 * This class is used directly by PrimaryIndex, not via an interface.  To avoid
 * making a public interface, the PersistEntityBinding contains a reference to
 * a PersistKeyAssigner, and the PrimaryIndex gets the key assigner from the
 * binding.  See the PrimaryIndex constructor for more information.
 *
 * @author Mark Hayes
 */
public class PersistKeyAssigner {

    /* See Store.refresh for an explanation of the use of volatile fields. */
    private volatile Catalog catalog;
    private volatile Format keyFieldFormat;
    private volatile Format entityFormat;
    private final boolean rawAccess;
    private final SSequence sequence;

    PersistKeyAssigner(PersistKeyBinding keyBinding,
                       PersistEntityBinding entityBinding,
                       SSequence sequence) {
        catalog = keyBinding.catalog;
        /* getSequenceKeyFormat will validate the field type for a sequence. */
        keyFieldFormat = keyBinding.keyFormat.getSequenceKeyFormat();
        entityFormat = entityBinding.entityFormat;
        rawAccess = entityBinding.rawAccess;
        this.sequence = sequence;
    }

    public boolean assignPrimaryKey(Object entity, SDatabaseEntry key)
        throws SDatabaseException {

        try {
            return assignPrimaryKeyInternal(entity, key);
        } catch (RefreshException e) {
            e.refresh();
            try {
                return assignPrimaryKeyInternal(entity, key);
            } catch (RefreshException e2) {
                throw DbCompat.unexpectedException(e2);
            }
        }
    }

    private boolean assignPrimaryKeyInternal(Object entity, SDatabaseEntry key)
        throws SDatabaseException, RefreshException {
            
        /*
         * The keyFieldFormat is the format of a simple integer field.  For a
         * composite key class it is the contained integer field.  By writing
         * the Long sequence value using that format, the output data can then
         * be read to construct the actual key instance, whether it is a simple
         * or composite key class, and assign it to the primary key field in
         * the entity object.
         */
        if (entityFormat.isPriKeyNullOrZero(entity, rawAccess)) {
            Long value = sequence.get(null, 1);
            RecordOutput output = new RecordOutput(catalog, rawAccess);
            keyFieldFormat.writeObject(value, output, rawAccess);
            TupleBase.outputToEntry(output, key);
            EntityInput input = new RecordInput
                (catalog, rawAccess, null, 0,
                 key.getData(), key.getOffset(), key.getSize());
            entityFormat.getReader().readPriKey(entity, input, rawAccess);
            return true;
        } else {
            return false;
        }
    }

    /**
     * See Store.refresh.
     */
    void refresh(final PersistCatalog newCatalog) {
        catalog = newCatalog;
        entityFormat = catalog.getFormat(entityFormat.getClassName());
        keyFieldFormat = catalog.getFormat(keyFieldFormat.getClassName());
    }
}
