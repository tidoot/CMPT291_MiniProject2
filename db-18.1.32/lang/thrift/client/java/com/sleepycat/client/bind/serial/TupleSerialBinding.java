/*-
 * Copyright (c) 2000, 2019 Oracle and/or its affiliates.  All rights reserved.
 *
 * See the file LICENSE for license information.
 *
 */

package com.sleepycat.client.bind.serial;

import com.sleepycat.client.bind.EntityBinding;
import com.sleepycat.client.bind.tuple.TupleBase;
import com.sleepycat.client.bind.tuple.TupleInput;
import com.sleepycat.client.bind.tuple.TupleOutput;
import com.sleepycat.client.SDatabaseEntry;

/**
 * An abstract <code>EntityBinding</code> that treats an entity's key entry as
 * a tuple and its data entry as a serialized object.
 *
 * <p>This class takes care of serializing and deserializing the data entry,
 * and converting the key entry to/from {@link TupleInput} and {@link
 * TupleOutput} objects.  Its three abstract methods must be implemented by a
 * concrete subclass to convert these objects to/from an entity object.</p>
 * <ul>
 * <li> {@link #entryToObject(TupleInput,Object)} </li>
 * <li> {@link #objectToKey(Object,TupleOutput)} </li>
 * <li> {@link #objectToData(Object)} </li>
 * </ul>
 *
 * @see <a href="SerialBinding.html#evolution">Class Evolution</a>
 *
 * @author Mark Hayes
 */
public abstract class TupleSerialBinding<D,E> extends TupleBase
    implements EntityBinding<E> {

    protected SerialBinding<D> dataBinding;

    /**
     * Creates a tuple-serial entity binding.
     *
     * @param classCatalog is the catalog to hold shared class information and
     * for a database should be a {@link StoredClassCatalog}.
     *
     * @param baseClass is the base class.
     */
    public TupleSerialBinding(ClassCatalog classCatalog,
                              Class<D> baseClass) {

        this(new SerialBinding<D>(classCatalog, baseClass));
    }

    /**
     * Creates a tuple-serial entity binding.
     *
     * @param dataBinding is the data binding.
     */
    public TupleSerialBinding(SerialBinding<D> dataBinding) {

        this.dataBinding = dataBinding;
    }

    // javadoc is inherited
    public E entryToObject(SDatabaseEntry key, SDatabaseEntry data) {

        return entryToObject(entryToInput(key),
                             dataBinding.entryToObject(data));
    }

    // javadoc is inherited
    public void objectToKey(E object, SDatabaseEntry key) {

        TupleOutput output = getTupleOutput(object);
        objectToKey(object, output);
        outputToEntry(output, key);
    }

    // javadoc is inherited
    public void objectToData(E object, SDatabaseEntry data) {

        D dataObject = objectToData(object);
        dataBinding.objectToEntry(dataObject, data);
    }

    /**
     * Constructs an entity object from {@link TupleInput} key entry and
     * deserialized data entry objects.
     *
     * @param keyInput is the {@link TupleInput} key entry object.
     *
     * @param dataInput is the deserialized data entry object.
     *
     * @return the entity object constructed from the key and data.
     */
    public abstract E entryToObject(TupleInput keyInput, D dataInput);

    /**
     * Extracts a key tuple from an entity object.
     *
     * @param object is the entity object.
     *
     * @param keyOutput is the {@link TupleOutput} to which the key should be
     * written.
     */
    public abstract void objectToKey(E object, TupleOutput keyOutput);

    /**
     * Extracts a data object from an entity object.
     *
     * @param object is the entity object.
     *
     * @return the deserialized data object.
     */
    public abstract D objectToData(E object);
}
